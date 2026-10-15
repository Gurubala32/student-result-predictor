from pathlib import Path
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "student_model.pkl"
RANDOM_SEED = 42

def main():
    rng = np.random.default_rng(RANDOM_SEED)
    sample_count = 1000

    study_hours = rng.uniform(0, 10, sample_count)
    attendance = rng.uniform(30, 100, sample_count)
    internal_marks = rng.uniform(0, 100, sample_count)

    # Create sample labels using a transparent rule, with a little realistic variation.
    points = (
        (study_hours >= 3).astype(int)
        + (attendance >= 75).astype(int)
        + (internal_marks >= 40).astype(int)
    )
    pass_probability = np.where(points >= 2, 0.90, 0.10)
    labels = (rng.random(sample_count) < pass_probability).astype(int)

    features = np.column_stack((study_hours, attendance, internal_marks))
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.2, random_state=RANDOM_SEED, stratify=labels
    )

    model = RandomForestClassifier(n_estimators=150, random_state=RANDOM_SEED)
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))
    with MODEL_PATH.open("wb") as model_file:
        pickle.dump(model, model_file)

    version_file = BASE_DIR / "VERSION"
    if not version_file.exists():
        version_file.write_text("1.0\n", encoding="utf-8")

    print("Student Result Predictor model trained successfully.")
    print(f"Model Version: {version_file.read_text(encoding='utf-8').strip()}")
    print(f"Test accuracy: {accuracy * 100:.2f}%")
    print(f"Model saved to: {MODEL_PATH}")

if __name__ == "__main__":
    main()
