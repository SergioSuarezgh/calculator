pipeline {
  agent any

  environment {
    GITHUB_OWNER = 'SergioSuarezgh'
    GITHUB_REPO  = 'calculator'
    IMAGE_NAME   = 'sergiosuarezgh/calculator'
  }

  stages {
    stage('Prepare') {
      steps {
        sh 'chmod +x gradlew'
      }
    }

    stage('Compile') {
      steps {
        sh './gradlew compileJava'
      }
    }

    stage('Unit test') {
      steps {
        sh './gradlew test'
      }
    }

    stage('Code coverage') {
      steps {
        sh './gradlew jacocoTestReport'

        publishHTML(target: [
          reportDir: 'build/reports/jacoco/test/html',
          reportFiles: 'index.html',
          reportName: 'JaCoCo Report'
        ])

        sh './gradlew jacocoTestCoverageVerification'
      }
    }

    stage('Package') {
      steps {
        sh './gradlew build'
      }
    }

    stage('Docker build') {
      steps {
        sh 'docker --version'
        sh "docker build -t ${IMAGE_NAME} ."
      }
    }
  }

  post {
    always {
      script {
        echo "Build result: ${currentBuild.currentResult}"
      }
    }
  }
}