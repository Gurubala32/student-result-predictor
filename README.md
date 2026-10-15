# Student Result Predictor

A sample Flask + scikit-learn project that predicts **Pass** or **Fail** from study hours, attendance percentage, and internal marks.

## Project structure

```text
student-result-predictor/
├── app.py
├── train.py
├── requirements.txt
├── Dockerfile
├── appspec.yml
├── VERSION
├── .gitignore
├── .dockerignore
├── templates/
│   └── index.html
└── scripts/
    ├── stop_container.sh
    └── start_container.sh
```

## Run locally on Windows

Open this folder in VS Code. In the VS Code terminal, run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python train.py
python app.py
```

Open `http://127.0.0.1:5000`.

If PowerShell blocks virtual-environment activation, run `python -m pip install -r requirements.txt` without activating it, then continue.

## Docker

```powershell
docker build -t student-result-predictor .
docker run --rm -p 5000:5000 student-result-predictor
```

Open `http://localhost:5000`.

## Version update

Change the content of `VERSION` from `1.0` to `2.0`, then commit and push the change. The deployment workflow rebuilds the Docker image and redeploys the app. The model version is read from this file when the application starts.

## AWS deployment files

`appspec.yml` and `scripts/` are a CodeDeploy starter setup for a Linux EC2 instance with Docker installed and a CodeDeploy agent configured. The EC2 instance needs inbound HTTP access on port 80. Configure the CodePipeline source and CodeDeploy deployment group separately in AWS.

## Important

The model is trained on generated sample data for demonstration only. It is not a validated academic prediction model.
