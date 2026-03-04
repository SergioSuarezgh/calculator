pipeline {
  agent any

  environment {
    // Cambia esto:
    GITHUB_OWNER = 'TU_ORG_O_USUARIO'
    GITHUB_REPO  = 'TU_REPO'
  }

  stages {
    stage('Compile') {
      steps {
        sh '''
          chmod +x gradlew
          ./gradlew compileJava
        '''
      }
    }

    stage('Unit test') {
      steps {
        sh '''
          chmod +x gradlew
          ./gradlew test
        '''
      }
    }

    stage('Code coverage') {
      steps {
        sh '''
          chmod +x gradlew
          ./gradlew jacocoTestReport
        '''

        publishHTML(target: [
          reportDir: 'build/reports/jacoco/test/html',
          reportFiles: 'index.html',
          reportName: 'JaCoCo Report'
        ])

        sh '''
          chmod +x gradlew
          ./gradlew jacocoTestCoverageVerification
        '''
      }
    }
  }

  post {
    always {
      // Publica un check en GitHub con el resultado del build
      publishChecks name: 'jenkins/ci',
        conclusion: currentBuild.currentResult,
        detailsURL: env.BUILD_URL
    }
  }
}