pipeline {
    agent any

    environment {
        // --- CONFIGURATION ---
        DOCKER_HUB_USER = 'rishabh720'
        IMAGE_NAME      = 'vqa-project'
        IMAGE_TAG       = "v3-${BUILD_NUMBER}"
        
        // --- NEW: POINT JENKINS TO YOUR LOCAL CLUSTER ---
        // This tells Minikube where to find the cluster state
        MINIKUBE_HOME = '/home/rishabh/.minikube'
        
        // This tells Ansible/Kubectl where to find connection details
        KUBECONFIG    = '/home/rishabh/.kube/config'
    }

    stages {
        // Stage 1: Fetches Code (Prerequisite for automated processes [cite: 17])
        stage('Checkout & Setup') {
            steps {
                checkout scm
            }
        }


        stage('CI: LoRA Simulation') {
            steps {
                echo "Starting LoRA Finetuning Simulation..."
                
                // --- FIX: Force CPU-only Torch installation first ---
                sh 'pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu'
                
                // Now install the rest (transformers will see torch is already there and skip it)
                sh 'pip install -r requirements.txt' 
                
                sh 'python3 src/train_mini.py'
            }
            post {
                always {
                    archiveArtifacts artifacts: '*.png', allowEmptyArchive: true
                }
            }
        }


        stage('Build Docker Images') {
            steps {
                script {
                    echo "1. Building App Image..."
                    // Standard build for the application logic
                    appImage = docker.build("${DOCKER_HUB_USER}/vqa-app:${IMAGE_TAG}")
                    
                    echo "2. Building Model Image (Layer-by-Layer Storage)..."
                    // Uses the specific Dockerfile.model to package the weights
                    modelImage = docker.build("${DOCKER_HUB_USER}/vqa-model:${IMAGE_TAG}", "-f Dockerfile.model .")
                }
            }
        }

        stage('CI: Model Evaluation') {
            steps {
                script {
                    echo "Validating Model Logic inside Container..."
                    
                    // --- THE FIX IS HERE ---
                    // We explicitly mount the host folder (/home/rishabh/...) 
                    // into the container folder (/app/data)
                    def dataPath = "/home/rishabh/Final Project/data"
                    
                    appImage.inside("-v \"${dataPath}\":/app/data") {
                        sh 'python3 src/evaluate_model.py'
                    }
                }
            }
        }

        stage('CD: Push to Registry') {
            steps {
                script {
                    echo "Pushing Images to Docker Hub..."
                    docker.withRegistry('', 'docker-hub-credentials-id') {
                        // Push App
                        appImage.push()
                        appImage.push('latest')
                        
                        // Push Model
                        modelImage.push()
                        modelImage.push('latest')
                    }
                }
            }
        }

        stage('CD: Deploy to Kubernetes') {
            steps {
                echo "Deploying..."
                sh 'pip install ansible kubernetes' 
                
                // Load BOTH images into Minikube to bypass network issues
                sh "minikube image load ${DOCKER_HUB_USER}/vqa-app:${IMAGE_TAG}"
                sh "minikube image load ${DOCKER_HUB_USER}/vqa-model:${IMAGE_TAG}"
                
                sh """
                ansible-playbook playbooks/deploy.yml \
                --extra-vars "image_tag=${IMAGE_TAG} docker_user=${DOCKER_HUB_USER}"
                """
            }
        }
    }
}