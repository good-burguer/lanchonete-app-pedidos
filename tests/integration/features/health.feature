Feature: Health endpoints

  Scenario: Health check returns ok
    When eu executo GET em "/health/"
    Then o status da resposta deve ser 200
    And o corpo JSON deve conter {"status": "ok"}

  Scenario: Health db check returns connected when dependency overridden
    Given eu sobrescrevo dependência get_db
    When eu executo GET em "/health/db"
    Then o status da resposta deve ser 200
    And o corpo JSON deve conter {"status": "connected"}
