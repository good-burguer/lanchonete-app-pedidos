Feature: Pedidos API

  Scenario: Criar pedido com sucesso
    Given o gateway de pedidos retorna um pedido válido
    And o gateway de pedido_produto retorna os produtos [1, 2]
    When eu envio um POST para "/pedidos/" com o payload
      | cliente_id | produtos     |
      | 42         | [1, 2]       |
    Then o status da resposta deve ser 201
    And o campo "status" do JSON deve ser "success"
    And o campo "data.produtos" do JSON deve ser [1, 2]

  Scenario: Listar pedidos retorna lista
    Given o gateway de pedidos retorna uma lista de pedidos
    When eu executo GET em "/pedidos/"
    Then o status da resposta deve ser 200
    And o campo "status" do JSON deve estar em ("success", "sucess")

  Scenario: Buscar pedido inexistente retorna 404
    Given o gateway de pedidos lança ValueError ao buscar por id
    When eu executo GET em "/pedidos/999"
    Then o status da resposta deve ser 404
