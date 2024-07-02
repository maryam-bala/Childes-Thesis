# Import libraries
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling, AdamW, get_scheduler

# Specify GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Specify the paths to train and validation datasets
train_data_path = "childes-train.txt"
val_data_path = "childes-val.txt"

# Set up the models and tokenizers
models = {
    "opt": {
        "model_checkpoint": "facebook/opt-350m",
        "output_dir": "finetuned_models/opt",
    },
    "dialogpt": {
        "model_checkpoint": "microsoft/DialoGPT-medium",
        "output_dir": "finetuned_models/dialogpt",
    },
}

# Fine-tune each model
for model_name, model_info in models.items():
    print(f"Fine-tuning {model_name}...")
    # Load the pre-trained model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_info["model_checkpoint"], use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(model_info["model_checkpoint"]).to(device)
    #model = model.to(device) 

    # Define a function that calls the tokenizer on texts
    def tokenize_function(examples):
        return tokenizer(examples["text"])

    # Load data with dataset
    datasets = load_dataset("text", data_files={"train": train_data_path, "validation": val_data_path})

    # Apply function to all the splits in our datasets object
    tokenized_datasets = datasets.map(tokenize_function, 
                                      batched=True, 
                                      num_proc=None, 
                                      remove_columns=["text"])

    # Define block size
    block_size = 128
    #block_size = min(tokenizer.model_max_length, 1024)

    # Preprocessing function to group texts
    def group_texts(examples):
        # Concatenate all texts.
        concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
        total_length = len(concatenated_examples[list(examples.keys())[0]])
        total_length = (total_length // block_size) * block_size

        # Split by chunks of max_len.
        result = {
            k: [t[i: i + block_size] for i in range(0, total_length, block_size)]
            for k, t in concatenated_examples.items()
        }
        result["labels"] = result["input_ids"].copy()
        return result
    
    # Speed-up the preprocessing by using multiprocessing
    lm_datasets = tokenized_datasets.map(
        group_texts,
        batched=True,
        num_proc=None
    )

    # Create data collator
    tokenizer.pad_token = tokenizer.eos_token
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    # Define training arguments
    training_args = TrainingArguments(
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        num_train_epochs=5,
        do_eval=True,
        evaluation_strategy="steps", 
        eval_steps=50,  
        load_best_model_at_end=True,
        save_strategy="steps", 
        save_total_limit=1,
        metric_for_best_model="eval_loss",
        logging_dir=model_info["output_dir"],
        logging_steps=50,
        save_steps=50, 
        output_dir=model_info["output_dir"],
    )

    # Create the trainer
    trainer = Trainer(
        model=model,
        tokenizer=tokenizer,
        args=training_args,
        train_dataset=lm_datasets["train"],
        eval_dataset=lm_datasets["validation"],
        data_collator=data_collator,
    )

    # Fine-tune the model
    trainer.train()

    # Save the fine-tuned model
    trainer.save_model(model_info["output_dir"])

    # Save the trainer state
    trainer.save_state()

    print("Fine-tuning completed.")