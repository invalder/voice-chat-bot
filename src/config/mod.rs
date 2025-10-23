//! Configuration management for voice chat bot
//! 
//! Provides strongly-typed configuration with YAML support

use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;
use anyhow::{Context, Result};

/// Speech-to-Text configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SttConfig {
    /// Whisper model size: tiny, base, small, medium, large
    #[serde(default = "default_model_name")]
    pub model_name: String,
    
    /// Language code for transcription (e.g., "en")
    #[serde(default = "default_language")]
    pub language: String,
}

impl Default for SttConfig {
    fn default() -> Self {
        Self {
            model_name: default_model_name(),
            language: default_language(),
        }
    }
}

/// Text-to-Speech configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TtsConfig {
    /// TTS engine: "pyttsx3" or "gtts"
    #[serde(default = "default_engine")]
    pub engine: String,
    
    /// Speech rate in words per minute
    #[serde(default = "default_rate")]
    pub rate: u32,
}

impl Default for TtsConfig {
    fn default() -> Self {
        Self {
            engine: default_engine(),
            rate: default_rate(),
        }
    }
}

/// RAG (Retrieval-Augmented Generation) configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RagConfig {
    /// Sentence transformer model for embeddings
    #[serde(default = "default_embedding_model")]
    pub embedding_model: String,
    
    /// Document chunk size in characters
    #[serde(default = "default_chunk_size")]
    pub chunk_size: usize,
    
    /// Overlap between chunks in characters
    #[serde(default = "default_chunk_overlap")]
    pub chunk_overlap: usize,
    
    /// Number of documents to retrieve
    #[serde(default = "default_top_k")]
    pub top_k: usize,
    
    /// Minimum similarity score (0.0-1.0)
    #[serde(default = "default_similarity_threshold")]
    pub similarity_threshold: f32,
}

impl Default for RagConfig {
    fn default() -> Self {
        Self {
            embedding_model: default_embedding_model(),
            chunk_size: default_chunk_size(),
            chunk_overlap: default_chunk_overlap(),
            top_k: default_top_k(),
            similarity_threshold: default_similarity_threshold(),
        }
    }
}

/// Main voice chat bot configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VoiceChatBotConfig {
    /// Speech-to-text configuration
    #[serde(default)]
    pub stt: SttConfig,
    
    /// Text-to-speech configuration
    #[serde(default)]
    pub tts: TtsConfig,
    
    /// RAG system configuration
    #[serde(default)]
    pub rag: RagConfig,
    
    /// Path to knowledge base directory
    #[serde(default = "default_knowledge_base_path")]
    pub knowledge_base_path: String,
    
    /// Path to vector database storage
    #[serde(default = "default_db_path")]
    pub db_path: String,
    
    /// Expert domain identifier
    #[serde(default = "default_expert_domain")]
    pub expert_domain: String,
}

impl Default for VoiceChatBotConfig {
    fn default() -> Self {
        Self {
            stt: SttConfig::default(),
            tts: TtsConfig::default(),
            rag: RagConfig::default(),
            knowledge_base_path: default_knowledge_base_path(),
            db_path: default_db_path(),
            expert_domain: default_expert_domain(),
        }
    }
}

impl VoiceChatBotConfig {
    /// Load configuration from YAML file
    pub fn from_yaml<P: AsRef<Path>>(path: P) -> Result<Self> {
        let content = fs::read_to_string(path.as_ref())
            .context("Failed to read config file")?;
        let config: Self = serde_yaml::from_str(&content)
            .context("Failed to parse config YAML")?;
        Ok(config)
    }
    
    /// Save configuration to YAML file
    pub fn to_yaml<P: AsRef<Path>>(&self, path: P) -> Result<()> {
        let content = serde_yaml::to_string(self)
            .context("Failed to serialize config")?;
        fs::write(path.as_ref(), content)
            .context("Failed to write config file")?;
        Ok(())
    }
}

// Default value functions
fn default_model_name() -> String { "tiny".to_string() }
fn default_language() -> String { "en".to_string() }
fn default_engine() -> String { "native".to_string() }
fn default_rate() -> u32 { 150 }
fn default_embedding_model() -> String { "all-MiniLM-L6-v2".to_string() }
fn default_chunk_size() -> usize { 500 }
fn default_chunk_overlap() -> usize { 50 }
fn default_top_k() -> usize { 3 }
fn default_similarity_threshold() -> f32 { 0.7 }
fn default_knowledge_base_path() -> String { "knowledge_base".to_string() }
fn default_db_path() -> String { "vector_db".to_string() }
fn default_expert_domain() -> String { "general".to_string() }

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_default_config() {
        let config = VoiceChatBotConfig::default();
        assert_eq!(config.expert_domain, "general");
        assert_eq!(config.stt.model_name, "tiny");
        assert_eq!(config.rag.top_k, 3);
    }
    
    #[test]
    fn test_config_serialization() {
        let config = VoiceChatBotConfig::default();
        let yaml = serde_yaml::to_string(&config).unwrap();
        assert!(yaml.contains("expert_domain"));
    }
}
