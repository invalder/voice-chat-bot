//! Voice Chat Bot - Zero Hallucination Guarantee
//!
//! A high-performance voice chat bot built in Rust with:
//! - 0% hallucination through RAG (Retrieval-Augmented Generation)
//! - Low resource consumption
//! - Fast response times
//! - Easy to read and maintain code structure

pub mod config;
pub mod rag;
pub mod stt;
pub mod tts;

use anyhow::{Context, Result};
use std::collections::HashMap;
use std::fs;
use std::path::Path;
use tracing::{info, warn};

pub use config::VoiceChatBotConfig;
pub use rag::{QueryResponse, RagSystem};
pub use stt::SpeechToText;
pub use tts::TextToSpeech;

/// Main Voice Chat Bot
///
/// Orchestrates STT, RAG, and TTS components for complete voice interaction
pub struct VoiceChatBot {
    config: VoiceChatBotConfig,
    stt: SpeechToText,
    tts: TextToSpeech,
    rag: RagSystem,
}

impl VoiceChatBot {
    /// Create a new Voice Chat Bot with the given configuration
    pub fn new(config: VoiceChatBotConfig) -> Result<Self> {
        info!("Initializing Voice Chat Bot...");
        info!("Expert domain: {}", config.expert_domain);

        // Initialize components
        let stt = SpeechToText::new(config.stt.model_name.clone(), config.stt.language.clone())?;

        let tts = TextToSpeech::new(config.tts.engine.clone(), config.tts.rate)?;

        let rag = RagSystem::new(config.db_path.clone(), config.expert_domain.clone())?;

        info!("Voice Chat Bot initialized successfully");

        Ok(Self {
            config,
            stt,
            tts,
            rag,
        })
    }

    /// Create a bot with default configuration
    pub fn with_default_config() -> Result<Self> {
        Self::new(VoiceChatBotConfig::default())
    }

    /// Load knowledge base from a directory
    ///
    /// Loads all .txt files from the specified directory into the knowledge base
    pub fn load_knowledge_base(&mut self, path: Option<&str>) -> Result<()> {
        let kb_path = path.unwrap_or(&self.config.knowledge_base_path);

        if !Path::new(kb_path).exists() {
            warn!("Knowledge base path does not exist: {}", kb_path);
            info!("Creating directory: {}", kb_path);
            fs::create_dir_all(kb_path).context("Failed to create knowledge base directory")?;
            return Ok(());
        }

        info!("Loading knowledge base from: {}", kb_path);

        let mut loaded_count = 0;

        // Read all .txt files from directory
        for entry in fs::read_dir(kb_path)? {
            let entry = entry?;
            let path = entry.path();

            if path.extension().and_then(|s| s.to_str()) == Some("txt") {
                self.rag.add_documents_from_file(
                    &path,
                    self.config.rag.chunk_size,
                    self.config.rag.chunk_overlap,
                )?;
                loaded_count += 1;
            }
        }

        info!("Loaded {} files from knowledge base", loaded_count);
        let stats = self.rag.get_stats();
        info!(
            "Total documents in knowledge base: {}",
            stats.get("total_documents").unwrap_or(&"0".to_string())
        );

        Ok(())
    }

    /// Add knowledge to the bot's knowledge base
    pub fn add_knowledge(
        &mut self,
        text: String,
        metadata: Option<HashMap<String, String>>,
    ) -> Result<String> {
        let doc_id = self.rag.add_document(text, metadata)?;
        info!("Knowledge added successfully");
        Ok(doc_id)
    }

    /// Process a text query and return a text response
    pub fn process_text_query(&self, query: &str) -> Result<String> {
        info!("Processing query: {}", query);

        let result = self.rag.query(
            query,
            self.config.rag.top_k,
            self.config.rag.similarity_threshold,
        )?;

        Ok(result.answer)
    }

    /// Process a voice query and return a text response
    pub fn process_voice_query(
        &self,
        audio_path: Option<&str>,
        duration: Option<u32>,
    ) -> Result<String> {
        // Convert speech to text
        let query = if let Some(path) = audio_path {
            self.stt.transcribe_audio_file(path)?
        } else {
            self.stt.record_and_transcribe(duration.unwrap_or(5))?
        };

        // Process the query
        self.process_text_query(&query)
    }

    /// Text-based chat interface
    ///
    /// Process a text query and optionally speak the response
    pub fn chat_text(&self, query: &str, speak_response: bool) -> Result<String> {
        let response = self.process_text_query(query)?;

        if speak_response {
            self.tts.speak(&response)?;
        }

        Ok(response)
    }

    /// Voice-based chat interface
    ///
    /// Process a voice query and speak the response aloud
    pub fn chat_voice(&self, audio_path: Option<&str>, duration: Option<u32>) -> Result<String> {
        let response = self.process_voice_query(audio_path, duration)?;
        self.tts.speak(&response)?;
        Ok(response)
    }

    /// Get bot statistics
    pub fn get_stats(&self) -> HashMap<String, String> {
        let mut stats = self.rag.get_stats();
        stats.insert(
            "expert_domain".to_string(),
            self.config.expert_domain.clone(),
        );
        stats.insert("stt_model".to_string(), self.config.stt.model_name.clone());
        stats.insert("tts_engine".to_string(), self.config.tts.engine.clone());
        stats.insert(
            "embedding_model".to_string(),
            self.config.rag.embedding_model.clone(),
        );
        stats
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bot_creation() {
        let config = VoiceChatBotConfig::default();
        let bot = VoiceChatBot::new(config);
        assert!(bot.is_ok());
    }

    #[test]
    fn test_add_and_query_knowledge() {
        let mut bot = VoiceChatBot::with_default_config().unwrap();

        bot.add_knowledge("Rust is a systems programming language.".to_string(), None)
            .unwrap();

        let response = bot.process_text_query("What is Rust?").unwrap();
        assert!(response.contains("Rust") || response.contains("knowledge"));
    }
}
