pipeline {
    agent any
    stages { 
        stage("Compile") {
            steps {
               sh '''
              chmod +x gradlew
              ./gradlew compileJava
            '''
          }
        }
        stage("Unit test") {
            steps {
                sh "./gradlew test"
            }
        }
        stage ("Code coverage") {
	  steps {
		sh "./gradlew jacocoTestReport"
		publishHTML (target: [
		  reportDir: 'build/reports/jacoco/test/html',
		  reportFiles: 'index.html',
		  reportName: "JaCoCo Report"
		])
		sh "./gradlew jacocoTestCoverageVerification"
 	  }	
	}

     }
post {
    success {
      setGitHubPullRequestStatus context: 'jenkins/ci', state: 'success', description: 'Build OK'
    }
    failure {
      setGitHubPullRequestStatus context: 'jenkins/ci', state: 'failure', description: 'Build FAILED'
    }
    unstable {
      setGitHubPullRequestStatus context: 'jenkins/ci', state: 'failure', description: 'Build UNSTABLE'
    }
  }}