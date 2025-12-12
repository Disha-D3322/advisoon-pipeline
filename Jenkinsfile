pipeline {
  agent any

  environment {
    LOG_DIR = "C:\\tmp\\advisoon-logs"
  }

  stages {
    stage('init') {
      steps {
        powershell """
          Write-Output '==== INIT ===='
          New-Item -ItemType Directory -Force -Path '${env.LOG_DIR}' | Out-Null
          \$ts = (Get-Date).ToString('yyyyMMddHHmmss')
          \$filepath = Join-Path -Path '${env.LOG_DIR}' -ChildPath ('init-' + \$ts + '.log')
          'Init at: ' + (Get-Date) | Out-File -FilePath \$filepath -Encoding utf8
          Write-Output ('Wrote init log to: ' + \$filepath)
        """
      }
    }

    stage('pre-check') {
      steps {
        powershell """
          Write-Output 'Checking Python availability...'
          \$py = (Get-Command python3 -ErrorAction SilentlyContinue).Path
          if (-not \$py) { \$py = (Get-Command python -ErrorAction SilentlyContinue).Path }
          if (-not \$py) {
            Write-Error 'Python not found on agent. Please install python3 or add python to PATH.'
            exit 1
          }
          Write-Output ('Using: ' + \$py)
          \$ts = (Get-Date).ToString('yyyyMMddHHmmss')
          \$pyfile = Join-Path -Path '${env.LOG_DIR}' -ChildPath ('python-version-' + \$ts + '.log')
          & \$py --version 2>&1 | Out-File -FilePath \$pyfile -Encoding utf8
          Write-Output ('Python version written to ' + \$pyfile)
        """
      }
    }

    stage('test') {
      steps {
        powershell """
          Write-Output 'Running unit tests...'
          \$ts = (Get-Date).ToString('yyyyMMddHHmmss')
          New-Item -ItemType Directory -Force -Path .\\reports | Out-Null
          New-Item -ItemType Directory -Force -Path .\\logs | Out-Null
          # Run pytest and store junit xml and stdout log
          python -m pytest -q --junitxml="reports\\junit-\$ts.xml" 2>&1 | Tee-Object -FilePath "logs\\pytest-\$ts.log"
          Write-Output 'pytest finished; junit and logs saved'
        """
      }
      post {
        always {
          junit 'reports/junit-*.xml'
        }
      }
    }

    stage('verify') {
      steps {
        powershell """
          Write-Output 'Verify: quick sample invocation'
          \$ts = (Get-Date).ToString('yyyyMMddHHmmss')
          python -c "from ad_scoring import score_ad; print(score_ad({'ctr':0.03,'relevance':0.9,'budget_ratio':0.7}))" > logs\\verify-\$ts.txt
          Write-Output ('Verify output saved to logs\\verify-' + \$ts + '.txt')
        """
      }
    }

    stage('publish') {
      steps {
        powershell """
          Write-Output 'Publishing artifacts...'
          New-Item -ItemType Directory -Force -Path '${env.LOG_DIR}' | Out-Null
          Copy-Item -Path .\\logs\\* -Destination '${env.LOG_DIR}' -Force -ErrorAction SilentlyContinue
          Copy-Item -Path .\\reports\\* -Destination '${env.LOG_DIR}' -Force -ErrorAction SilentlyContinue
          Write-Output ('Copied logs and reports to ${env.LOG_DIR}')
        """
      }
      post {
        success {
          archiveArtifacts artifacts: 'C:\\tmp\\advisoon-logs\\**', fingerprint: true
        }
        always {
          powershell "Get-ChildItem -Path '${env.LOG_DIR}' -Recurse | Select-Object FullName, LastWriteTime"
        }
      }
    }
  }

  post {
    always {
      echo "Pipeline finished at \$(date)"
    }
  }
}
