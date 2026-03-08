pipeline {
  agent any

  environment {
  GITHUB_OWNER = 'SergioSuarezgh'
  GITHUB_REPO  = 'calculator'
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

    stage('Package'){
      steps {
        sh "./gradlew build"
      }
    }

    stage('Docker build'){
      steps{
        sh "docker build -t sergiosuarezgh/calculator ."
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