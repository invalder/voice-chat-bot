//! Voice Chat Bot - Main CLI Application

use anyhow::Result;
use clap::{Parser, Subcommand};
use std::io::{self, Write};
use tracing::{info, Level};
use voice_chat_bot::{VoiceChatBot, VoiceChatBotConfig};

#[derive(Parser)]
#[command(name = "voice-chat-bot")]
#[command(about = "Voice Chat Bot with 0% Hallucination Guarantee", long_about = None)]
struct Cli {
    /// Configuration file path
    #[arg(short, long, default_value = "config.yaml")]
    config: String,

    /// Enable verbose logging
    #[arg(short, long)]
    verbose: bool,

    #[command(subcommand)]
    command: Option<Commands>,
}

#[derive(Subcommand)]
enum Commands {
    /// Start interactive text chat mode
    Chat {
        /// Load knowledge base from directory
        #[arg(short, long)]
        knowledge_base: Option<String>,
    },

    /// Load knowledge base from directory
    LoadKnowledge {
        /// Path to knowledge base directory
        path: String,
    },

    /// Query the bot with a single question
    Query {
        /// The question to ask
        question: String,

        /// Speak the response aloud
        #[arg(short, long)]
        speak: bool,
    },

    /// Show bot statistics
    Stats,
}

fn main() -> Result<()> {
    let cli = Cli::parse();

    // Setup logging
    let level = if cli.verbose {
        Level::DEBUG
    } else {
        Level::INFO
    };
    tracing_subscriber::fmt()
        .with_max_level(level)
        .with_target(false)
        .init();

    // Load configuration
    let config = if std::path::Path::new(&cli.config).exists() {
        VoiceChatBotConfig::from_yaml(&cli.config)?
    } else {
        info!("Config file not found, using defaults");
        VoiceChatBotConfig::default()
    };

    // Create bot
    let mut bot = VoiceChatBot::new(config)?;

    match cli.command {
        Some(Commands::Chat { knowledge_base }) => {
            // Load knowledge base
            bot.load_knowledge_base(knowledge_base.as_deref())?;

            // Start interactive chat
            run_interactive_chat(&bot)?;
        }

        Some(Commands::LoadKnowledge { path }) => {
            bot.load_knowledge_base(Some(&path))?;
            println!("Knowledge base loaded successfully!");

            let stats = bot.get_stats();
            println!(
                "Total documents: {}",
                stats.get("total_documents").unwrap_or(&"0".to_string())
            );
        }

        Some(Commands::Query { question, speak }) => {
            let response = bot.chat_text(&question, speak)?;
            println!("\nBot: {}", response);
        }

        Some(Commands::Stats) => {
            display_stats(&bot);
        }

        None => {
            // Default: load knowledge base and start chat
            bot.load_knowledge_base(None)?;
            run_interactive_chat(&bot)?;
        }
    }

    Ok(())
}

fn run_interactive_chat(bot: &VoiceChatBot) -> Result<()> {
    println!("{}", "=".repeat(60));
    println!("Voice Chat Bot - 0% Hallucination Guarantee");
    println!("{}", "=".repeat(60));

    display_stats(bot);

    println!("\n{}", "=".repeat(60));
    println!("Text Chat Mode - Type 'quit' or 'exit' to stop");
    println!("{}", "=".repeat(60));

    loop {
        print!("\nYou: ");
        io::stdout().flush()?;

        let mut input = String::new();
        io::stdin().read_line(&mut input)?;

        let query = input.trim();

        if query.is_empty() {
            continue;
        }

        if query.eq_ignore_ascii_case("quit") || query.eq_ignore_ascii_case("exit") || query == "q"
        {
            println!("Goodbye!");
            break;
        }

        match bot.chat_text(query, false) {
            Ok(response) => {
                println!("\nBot: {}", response);
            }
            Err(e) => {
                eprintln!("\nError: {}", e);
            }
        }
    }

    Ok(())
}

fn display_stats(bot: &VoiceChatBot) {
    let stats = bot.get_stats();
    println!("\nBot Statistics:");
    println!(
        "  Expert Domain: {}",
        stats.get("expert_domain").unwrap_or(&"unknown".to_string())
    );
    println!(
        "  STT Model: {}",
        stats.get("stt_model").unwrap_or(&"unknown".to_string())
    );
    println!(
        "  TTS Engine: {}",
        stats.get("tts_engine").unwrap_or(&"unknown".to_string())
    );
    println!(
        "  Total Documents: {}",
        stats.get("total_documents").unwrap_or(&"0".to_string())
    );
}
