#!/usr/bin/env python3
import argparse
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.rag_pipeline import RAGPipeline


def main():
    parser = argparse.ArgumentParser(description="Simple RAG System CLI")
    parser.add_argument("--ingest-file", type=str, help="Ingest a document file")
    parser.add_argument("--ingest-dir", type=str, help="Ingest all documents from directory")
    parser.add_argument("--ingest-text", type=str, help="Ingest raw text")
    parser.add_argument("--query", type=str, help="Query the RAG system")
    parser.add_argument("--info", action="store_true", help="Show system information")
    parser.add_argument("--interactive", action="store_true", help="Start interactive mode")
    
    args = parser.parse_args()
    
    rag = RAGPipeline()
    
    if args.info:
        info = rag.get_system_info()
        print("=== RAG System Information ===")
        print(f"Vector DB: {info['vector_db']['name']} ({info['vector_db']['document_count']} documents)")
        print(f"Embedding Model: {info['embedding_model']['model_name']}")
        print(f"LLM Provider: {info['llm']['provider']} ({info['llm']['model']})")
        return
    
    if args.ingest_file:
        print(f"Ingesting file: {args.ingest_file}")
        try:
            count = rag.ingest_document(args.ingest_file)
            print(f"Successfully ingested {count} chunks")
        except Exception as e:
            print(f"Error ingesting file: {e}")
        return
    
    if args.ingest_dir:
        print(f"Ingesting directory: {args.ingest_dir}")
        try:
            count = rag.ingest_directory(args.ingest_dir)
            print(f"Successfully ingested {count} chunks")
        except Exception as e:
            print(f"Error ingesting directory: {e}")
        return
    
    if args.ingest_text:
        print("Ingesting text...")
        try:
            count = rag.ingest_text(args.ingest_text)
            print(f"Successfully ingested {count} chunks")
        except Exception as e:
            print(f"Error ingesting text: {e}")
        return
    
    if args.query:
        print(f"Query: {args.query}")
        try:
            result = rag.query(args.query)
            print(f"\nAnswer: {result['answer']}")
            if result['sources']:
                print(f"\nSources ({len(result['sources'])}):")
                for i, source in enumerate(result['sources']):
                    print(f"  {i+1}. {source['metadata'].get('source_file', 'Unknown')}")
        except Exception as e:
            print(f"Error querying: {e}")
        return
    
    if args.interactive:
        print("=== Interactive RAG Mode ===")
        print("Type 'quit' or 'exit' to stop")
        print("Type 'info' for system information")
        print("Commands: ingest <file>, ingest-dir <dir>, query <question>")
        print()
        
        while True:
            try:
                user_input = input("RAG> ").strip()
                
                if user_input.lower() in ['quit', 'exit']:
                    print("Goodbye!")
                    break
                
                if user_input.lower() == 'info':
                    info = rag.get_system_info()
                    print(f"Documents: {info['vector_db']['document_count']}")
                    print(f"Model: {info['embedding_model']['model_name']}")
                    print(f"LLM: {info['llm']['provider']}")
                    continue
                
                if user_input.startswith('ingest '):
                    file_path = user_input[7:].strip()
                    print(f"Ingesting {file_path}...")
                    try:
                        count = rag.ingest_document(file_path)
                        print(f"Successfully ingested {count} chunks")
                    except Exception as e:
                        print(f"Error: {e}")
                    continue
                
                if user_input.startswith('ingest-dir '):
                    dir_path = user_input[10:].strip()
                    print(f"Ingesting directory {dir_path}...")
                    try:
                        count = rag.ingest_directory(dir_path)
                        print(f"Successfully ingested {count} chunks")
                    except Exception as e:
                        print(f"Error: {e}")
                    continue
                
                if user_input.startswith('query '):
                    question = user_input[6:].strip()
                    print(f"Querying: {question}")
                    try:
                        result = rag.query(question)
                        print(f"\nAnswer: {result['answer']}")
                        if result['sources']:
                            print(f"\nSources: {len(result['sources'])}")
                    except Exception as e:
                        print(f"Error: {e}")
                    continue
                
                # Default to query if no command
                if user_input:
                    print(f"Querying: {user_input}")
                    try:
                        result = rag.query(user_input)
                        print(f"\nAnswer: {result['answer']}")
                        if result['sources']:
                            print(f"\nSources: {len(result['sources'])}")
                    except Exception as e:
                        print(f"Error: {e}")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break
        
        return
    
    parser.print_help()


if __name__ == "__main__":
    main()