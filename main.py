import pandas as pd
from pathlib import Path
import datetime

# --- SETUP PATHS ---
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
NOTES_DIR = BASE_DIR / "notes"

def analyze_data(df):
    print("\n" + "="*30)
    print("📊 DATA INTELLIGENCE REPORT")
    print("="*30)
    
    df.columns = df.columns.str.strip()
    
    # Universal: Convert EVERY column to numeric if possible
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')

    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if not numeric_cols:
        print("❌ No numeric data found to analyze.")
        return

    # UNIVERSAL LOGIC: 
    # If there is a text column (like 'Car', 'Name', or 'Category'), group by it!
    if categorical_cols:
        main_cat = categorical_cols[0] # Pick the first text column found
        print(f"\n📈 Averages Grouped by: {main_cat}")
        print(df.groupby(main_cat)[numeric_cols].mean().round(2))
    
    print("\n🏆 Global Maximums:")
    print(df[numeric_cols].max())

def save_note(file_name):
    print("\n" + "-"*30)
    # Added the 'q' to quit option here
    topic = input("Enter Note Topic (or 'q' to skip note): ").strip()
    
    if topic.lower() in ['q', 'quit', 'exit']:
        print("⏭️ Skipping note taking.")
        return

    topic = topic.replace(" ", "_")
    note_content = input("Write your observation: ")
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    note_path = NOTES_DIR / f"{topic}.txt"
    
    with open(note_path, "a", encoding='utf-8') as f:
        f.write(f"\n--- Entry: {timestamp} ---\nSource: {file_name}\nNote: {note_content}\n")
    
    print(f"✅ Note saved to notes/{topic}.txt")

def main():
    DATA_DIR.mkdir(exist_ok=True)
    NOTES_DIR.mkdir(exist_ok=True)
    
    print("🚀 DataNotebook Pro: Online")
    files = list(DATA_DIR.glob("*.csv")) + list(DATA_DIR.glob("*.xlsx"))
    
    if not files:
        print(f"Empty! Drop your file in: {DATA_DIR}")
        return

    for i, f in enumerate(files):
        print(f"[{i}] {f.name}")
    
    choice = input("\nSelect file index: ")
    try:
        selected_file = files[int(choice)]
        
        # SMART LOAD: 'sep=None' tells pandas to guess if you used commas or spaces
        if selected_file.suffix == '.csv':
            df = pd.read_csv(selected_file, sep=r'\s+', engine='python', encoding='utf-8-sig')
        else:
            df = pd.read_excel(selected_file)

        print(f"\n✅ Successfully analyzed: {selected_file.name}")
        analyze_data(df)
        save_note(selected_file.name)
        
    except Exception as e:
        print(f"⚠️ An error occurred: {e}")

if __name__ == "__main__":
    main()