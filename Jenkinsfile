pipeline {
    agent any

    environment {
        // --- CONFIGURATION: Update these values ---
        DOCKER_HUB_USER = 'rishabh720'  // <--- REPLACE WITH YOUR ACTUAL USERNAME
        IMAGE_NAME      = 'vqa-project'
        IMAGE_TAG       = "v3-${BUILD_NUMBER}"       // Use a unique tag for every build
    }

    stages {
        // Stage 1: Fetches Code (Prerequisite for automated processes [cite: 17])
        stage('Checkout & Setup') {
            steps {
                checkout scm
            }
        }

        // Stage 2: CI Test (Requirement: "Running automated tests" [cite: 18])
        // stage('CI: LoRA Simulation') {
        //     steps {
        //         echo "Starting LoRA Finetuning Simulation..."
        //         sh 'pip install -r requirements.txt' 
        //         sh 'python3 src/train_mini.py'
        //     }
        //     post {
        //         always {
        //             // Archives the loss graph for visual proof
        //             archiveArtifacts artifacts: '*.png', allowEmptyArchive: true
        //         }
        //     }
        // }

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

        // Stage 3: Build Container
        // stage('Build Docker Image') {
        //     steps {
        //         script {
        //             echo "Building Docker Image..."
        //             // Uses the optimized Dockerfile (CPU-only, data excluded)
        //             customImage = docker.build("${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}")
        //         }
        //     }
        // }

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

        // Stage 4: Model Evaluation (Quality Gate)
        // stage('CI: Model Evaluation') {
        //     steps {
        //         script {
        //             echo "Validating Model Logic inside Container..."
        //             // Runs the evaluation script inside the container environment
        //             customImage.inside {
        //                 sh 'python3 src/evaluate_model.py'
        //             }
        //         }
        //     }
        // }
        // Stage 4: Model Evaluation (Quality Gate)
        // stage('CI: Model Evaluation') {
        //     steps {
        //         script {
        //             echo "Validating Model Logic inside Container..."
                    
        //             // FIX: Use 'appImage' instead of 'customImage'
        //             appImage.inside {
        //                 sh 'python3 src/evaluate_model.py'
        //             }
        //         }
        //     }
        // }

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

        // Stage 5: Push to Registry (Requirement: "Pushing... to Docker Hub" [cite: 19])
        // stage('CD: Push to Registry') {
        //     steps {
        //         script {
        //             echo "Pushing Image to Docker Hub..."
        //             // Requires "docker-hub-credentials" ID in Jenkins
        //             docker.withRegistry('', 'docker-hub-credentials') {
        //                 customImage.push()
        //                 customImage.push('latest')
        //             }
        //         }
        //     }
        // }

        // stage('CD: Push to Registry') {
        //     steps {
        //         script {
        //             docker.withRegistry('', 'docker-hub-credentials') {
        //                 // Push App
        //                 appImage.push()
        //                 appImage.push('latest')
                        
        //                 // Push Model (Stores weights in registry)
        //                 modelImage.push()
        //                 modelImage.push('latest')
        //             }
        //         }
        //     }
        // }

        // Stage 5: Push to Registry

        stage('CD: Push to Registry') {
            steps {
                script {
                    echo "Pushing Images to Docker Hub..."
                    docker.withRegistry('', 'docker-hub-credentials') {
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

        // Stage 6: Deployment (Requirement: "Deploying... to a target system" [cite: 20])
        // stage('CD: Deploy to Kubernetes') {
        //     steps {
        //         echo "Deploying with Ansible..."
        //         sh 'pip install ansible kubernetes' // Ensures tools are present
                
        //         // Runs Ansible to apply the deployment.yaml manifest
        //         sh """
        //         ansible-playbook playbooks/deploy.yml \
        //         --extra-vars "image_tag=${IMAGE_TAG} docker_user=${DOCKER_HUB_USER}"
        //         """
        //     }
        // }

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