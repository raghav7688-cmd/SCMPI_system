from .ai_model import train_and_save

if __name__ == "__main__":
    metrics = train_and_save()
    print(f"Model trained. R2: {metrics['r2']} saved to {metrics['path']}")

