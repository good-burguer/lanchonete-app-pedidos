Feature: StatusPedido API

  Scenario: Criar status com sucesso
    Given o gateway de status retorna um status válido
    When eu envio um POST para "/status_pedido/" com o payload
      | descricao |
      | Pronto    |
    Then o status da resposta deve ser 201
    And o campo "status" do JSON deve ser "success"

  Scenario: Buscar status inexistente retorna 404
    Given o gateway de status lança ValueError ao buscar por id
    When eu executo GET em "/status_pedido/999"
    Then o status da resposta deve ser 404
