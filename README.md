# Cloud-Native AI Receptionist

A highly scalable, production-grade intelligent assistant platform. This project features a containerized **Python microservices backend** orchestrated inside an **AWS EKS Kubernetes cluster**, provisioned securely via **Terraform (IaC)**, and continuously built, tested, and deployed using a fully automated **Jenkins CI/CD pipeline**.

---

## System & Pipeline Architecture

This diagram illustrates how code commits automatically flow through the Jenkins automated worker node, push container images securely into AWS ECR, and execute a zero-downtime rolling deployment to the AWS EKS Cluster pods.

```mermaid
graph TD
    %% CI/CD Pipeline
    subhost[Developer Commit] -->|Git Push| Git[GitHub Repository]
    Git -->|Webhook Trigger| Jenkins[Jenkins Pipeline Engine]
    
    subgraph Jenkins Build Agent
        J1[1. Verify Source Code] --> J2[2. Docker Build]
        J2 --> J3[3. Run Pytest Framework]
        J3 --> J4[4. AWS ECR Authentication]
        J4 --> J5[5. Docker Push Image]
        J5 --> J6[6. Kubeconfig Access Update]
        J6 --> J7[7. Kubectl Rolling Deploy]
    end
    
    Jenkins --> J1

    %% Cloud Infrastructure Target
    subgraph AWS Cloud Architecture (ap-south-1)
        ECR[(Amazon ECR Repository)]
        
        subgraph Amazon EKS Cluster (ai-receptionist-eks)
            subgraph K8s Namespace: ai-receptionist
                Ingress[K8s Service / Ingress]
                Deploy[Deployment: ai-receptionist]
                Pods[Application Pods / Containers]
                
                Ingress --> Deploy
                Deploy --> Pods
            end
        end
    end

    J5 -->|Uploads Image| ECR
    ECR -->|Pulls Image| Pods
    J7 -->|Triggers Rollout Set Image| Deploy
```

*Note: The interactive flowchart above is written in native **Mermaid.js** syntax and will visually render directly on the GitHub repository landing page.*

---

## Key Features & Engineering Highlights
* **Automated Infrastructure:** Full AWS public/private topology provisioning using **Terraform**, managing VPCs, subnets, routing tables, and EKS components.
* **Continuous Integration:** Automated verification phase checking for required application assets (`Dockerfile`, `requirements.txt`) prior to execution.
* **Quality Assurance Isolation:** Automated test suite runs **Python Pytest** execution inside the freshly built container isolated runtime environment before registry push operations.
* **Secure Image Registry:** Authenticates natively against **Amazon Elastic Container Registry (ECR)** inside the pipeline using dynamic AWS CLI tokens.
* **Zero-Downtime Rollout Strategy:** Leverages `kubectl set image` tracking updates combined with `rollout status` verification gates to enforce safe, blue-green style rolling application deployments.

---

## Repository Structure

* **`/backend`**: Core Python microservice backend application logic, dependency manifests (`requirements.txt`), unit test suites, and project Dockerfile.
* **`/k8s`**: Declarative Kubernetes resource configuration specifications managing deployment controllers, service discovery endpoints, and target namespaces.
* **`/terraform/eks`**: Declarative Infrastructure as Code scripts managing structural AWS network layout and target cluster sizing parameters.
* **`Jenkinsfile`**: Complete declarative multi-stage automation pipeline managing application lifecycle execution.

---

## Infrastructure Configuration & Specs
* **Cloud Region:** `ap-south-1` (Asia Pacific - Mumbai)
* **AWS Target ECR Path:** `://amazonaws.com`
* **EKS Cluster Target:** `ai-receptionist-eks`
* **K8s Deployment Runtime Object Target Namespace:** `ai-receptionist`

---

## CI/CD Pipeline Workflow Steps

The declarative `Jenkinsfile` controls execution flow through these validation checkpoints:

1. **Checkout:** Pulls source branches instantly upon build environment invocation.
2. **Verify Source:** Validation gate ensuring core system configurations exist across `/backend` and `/k8s` before executing compute stages.
3. **Docker Build:** Builds a unique application release package using the respective `${BUILD_NUMBER}` increment tag.
4. **Application Tests:** Boots up an ephemeral test container runner executing isolation integration checks via **Pytest**.
5. **Docker Login to ECR:** Securely authenticates local agent nodes against cloud registries using standard AWS access patterns.
6. **Push Image to ECR:** Registers the immutable version artifact up into the cloud registry storage systems.
7. **Verify EKS Access:** Generates EKS connection endpoints and conducts initial health status checks on worker infrastructure.
8. **Deploy to EKS:** Automates the production version shift command, waiting up to **180 seconds** to verify microservice stability markers.
9. **Verify Deployment:** Generates real-time post-deployment telemetry output printing live cluster topology conditions.

---

## How to Clean Up Local Agents
The configuration engine has a built-in clean-up trigger block executing post-pipeline states. This frees memory boundaries on your Jenkins nodes automatically after a pass or fail event:
```bash
docker image rm "\${IMAGE_NAME}" 2>/dev/null || true
docker image prune -f 2>/dev/null || true
```

