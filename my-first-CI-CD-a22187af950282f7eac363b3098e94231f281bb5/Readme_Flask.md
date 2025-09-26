# CI/CD Flask App Helm Chart
CI/CD pipeline for a containerized Flask application using Jenkins, GitLab, and Nexus.

##		Prerequisites

- Install Docker e Docker Compose 
- Immage base: Python 3.12-slim
- Access to GitLab
- Jenkins, Nexus, and GitLab running via `docker-compose.yaml`

##		Quick Start (TL;DR)

# Add required repository
	git clone 'https://gitlab.ko2.it/Tarallo/my-first-CI-CD.git'

# Move to the repo
	cd My-First-CI-CD/(new name)

# Repository Structure:

My-First-CI-CD/
│
├── app.py                     # Main Flask application
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Dockerfile per l'app Flask
├── docker-compose.yaml        # Docker Compose per Jenkins, GitLab, Nexus e app Flask
├── helm/                      # Helm chart directory
│   ├── Chart.yaml             # Metadata Helm chart
│   ├── values.yaml            # Configuration values for Helm chart
│   ├── templates/             # Kubernetes manifests templates
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── ingress.yaml
│   │   └── secret.yaml
│   └── README.md              # Optional: Helm chart documentation
├── jenkins/                   # Jenkins configuration files
│   ├── jobs/                  # Job definitions (XML or Pipeline scripts)
│   └── credentials.xml         # Credentials setup
├── gitlab/                    # GitLab specific configuration (optional)
│   └── .gitlab-ci.yml         # GitLab CI pipeline (if used)
├── nexus/                     # Nexus configuration (optional)
│   └── repositories.json       # Preconfigured repositories
├── README.md                  # Project README / documentation
└── scripts/                   # Utility scripts (build, deploy, test)
    ├── build.sh
    ├── deploy.sh
    └── test.sh


# Launch containers of: Gitlab Nexus and Jenkins
	docker-compose up -d

# Access services
	- Jenkins → http://localhost:8080
	- GitLab → http://localhost:443
	- Nexus → http://localhost:8081
	- Flask app → http://localhost:5000

# Installation (detailed, step by step)

	- [Docker-compose up -d] 
	# Start Service (container Nexus, Jenkins, GitLab)

	- Gitlab Configuration
	# ('https://gitlab.ko2.it/Tarallo/my-first-CI-CD.git', <key SSH>)

	- Jenkins Configuration and Login Credentials
	# (Creating Nexus login credentials, GitLab login credentials, plugins, first "raw(hosted)" job.) 

	- Nexus repository configuration 
	# (Hosted Nexus repositories, credentials)

	- Pipeline configuration
	# (step: build "app.py", git add ./commit/push, build job)
  


##		Running the Application Locally (Python)

# Create virtual environment
	python -m venv venv
	source venv/bin/activate

# Install dependencies
	pip install -r requirements.txt

# Run Flask app
	python app.py

# Access app at http://localhost:5000



##		Running with Docker
# Build Docker image
docker build -t app-flask:latest .

# Run container
docker run -p 5000:5000 flask-app:latest

# Access app at http://localhost:5000



##		Running with Docker Compose

# Start all services
docker-compose up -d

# Check running containers
docker ps

# Stop services
docker-compose down


#### Installing Helm Chart on Kubernetes ####

##		1. Create Namespace (optional)
kubectl create namespace flask-cicd

##		2. Create Docker Registry Secret
kubectl create secret docker-registry regcred \
  --namespace flask-cicd \
  --docker-server='YOUR_REGISTRY_SERVER' \
  --docker-username='YOUR_USERNAME' \
  --docker-password='YOUR_PASSWORD'

##		3. Install Helm Chart
helm install flask-app . -f values.yaml --namespace flask-cicd
----------------------------------------------------------------------------------
NOTES: Configure database, ingress, secrets, and other options via values.yaml or --set flags.
----------------------------------------------------------------------------------


### USEFUL COMMANDS ###
# Check pods
kubectl get pods -n flask-cicd

# Check ingress
kubectl get ingress -n flask-cicd

# Helm upgrade n replica
helm upgrade flask-app . --namespace flask-cicd --set backend.replicaCount=3

# Rollback Helm release
helm rollback flask-app <REVISION> -n flask-cicd


###	Troubleshooting
Pods pending → Check Logs resources and describe resources

Connection issues → Verify service names, ports, network policies

Image pull failures → Check registry credentials

Database issues → Check pod status and credentials


## 		Local Development Tips		##

# Debug inside container:
	docker exec -it <container_id> /bin/bash


# Virtual Environment:
Use venv for local Python testing to avoid conflicts.

# Hot Reload:
Mount the local folder inside Docker to auto-reload Flask changes:
	docker run -p 5000:5000 -v $(pwd):/app flask-app:latest



## CI/CD Pipeline Details ##

# Build:
 Jenkins job runs python app.py inside container.

# Test:
 Optional unit tests via pytest can be added to Jenkins pipeline.

# Push:
 Jenkins pushes Docker image to Nexus registry.

# Deploy:
 Helm upgrade command is triggered to deploy new version on Kubernetes.

# Automation:
 Jobs can be triggered by GitLab push, merge requests, or manual build.


## FAQ / Common Issues ##

# Pods pending:
 Check pod logs and resource descriptions:
	kubectl describe pod <pod-name> -n flask-cicd

# Connection issues:
 Verify service names, ports, and network policies.

# Image pull failures:
 Ensure correct Docker registry credentials and image tags.

# Database issues:
 Confirm pod status and credentials.

# Flask app not starting:
 Check dependencies and Python version.



-------------------------------------------------------------------------------------