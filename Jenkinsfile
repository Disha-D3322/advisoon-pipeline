pipeline {
  agent {
    docker {
      image 'python:3.11'
      args '-u root:root'
    }
  }

  environment {
    LOG_DIR = "/tmp/advisoon-logs"
  }

  stages {
    stage('init') {
      steps {
        sh '''
          set -e
          mkdir -p ${LOG_DIR}
          ts=$(date +%Y%m%d%H%M%S)
          echo "Init at $(date)" > ${LOG_DIR}/init-${ts}.log
        '''
      }
    }

    stage('pre-check') {
      steps {
        sh '''
          set -e
          python --version
          python --version | tee ${LOG_DIR}/python-version-$(date +%Y%m%d%H%M%S).log
        '''
      }
    }

    stage('test') {
      steps {
        sh '''
          set -e
          ts=$(date +%Y%m%d%H%M%S)
          pip install pytest pytest-cov >/dev/null
          mkdir -p reports logs
          python -m pytest -q --junitxml=reports/junit-${ts}.xml 2>&1 | tee logs/pytest-${ts}.log || true
        '''
      }
      post {
        always {
          junit 'reports/junit-*.xml'
        }
      }
    }

    stage('verify') {
      steps {
        sh '''
          ts=$(date +%Y%m%d%H%M%S)
          python -c "from ad_scoring import score_ad; print(score_ad({'ctr':0.03,'relevance':0.9,'budget_ratio':0.7}))" > logs/verify-${ts}.txt
        '''
      }
    }

    stage('publish') {
      steps {
        sh '''
          mkdir -p ${LOG_DIR}
          cp -v logs/* ${LOG_DIR}/ || true
          cp -v reports/* ${LOG_DIR}/ || true
        '''
      }
      post {
        success {
          archiveArtifacts artifacts: '/tmp/advisoon-logs/**', fingerprint: true
        }
      }
    }
  }
}
