# DER — Olist

Modelo lógico das nove tabelas CSV em `C:\Users\User\Desktop\Projects\olist`, com as colunas necessárias para entender as relações.

```mermaid
erDiagram
    CUSTOMERS ||--|| ORDERS : "customer_id"
    ORDERS ||--o{ ORDER_ITEMS : "order_id"
    ORDERS ||--o{ ORDER_PAYMENTS : "order_id"
    ORDERS ||--o{ ORDER_REVIEWS : "order_id"
    PRODUCTS ||--o{ ORDER_ITEMS : "product_id"
    SELLERS ||--o{ ORDER_ITEMS : "seller_id"
    CATEGORY_TRANSLATION |o--o{ PRODUCTS : "product_category_name"
    CUSTOMERS }o..o{ GEOLOCATION : "prefixo de CEP"
    SELLERS }o..o{ GEOLOCATION : "prefixo de CEP"

    CUSTOMERS {
        string customer_id PK
        string customer_unique_id
        string customer_zip_code_prefix
    }
    ORDERS {
        string order_id PK
        string customer_id FK
    }
    ORDER_ITEMS {
        string order_id PK, FK
        int order_item_id PK
        string product_id FK
        string seller_id FK
    }
    ORDER_PAYMENTS {
        string order_id PK, FK
        int payment_sequential PK
    }
    ORDER_REVIEWS {
        string review_id
        string order_id FK
    }
    PRODUCTS {
        string product_id PK
        string product_category_name FK
    }
    SELLERS {
        string seller_id PK
        string seller_zip_code_prefix
    }
    CATEGORY_TRANSLATION {
        string product_category_name PK
        string product_category_name_english
    }
    GEOLOCATION {
        string geolocation_zip_code_prefix
        float geolocation_lat
        float geolocation_lng
    }
```

- `PK`: chave primária lógica. Duas colunas marcadas com PK na mesma tabela formam uma chave composta.
- `FK`: coluna usada para relacionar tabelas; os CSVs não impõem restrições de banco de dados.
- `||`: exatamente um; `o{` ou `}o`: zero ou muitos; `|o`: zero ou um.
- `CATEGORY_TRANSLATION` representa `product_category_name_translation.csv`. Os demais nomes abreviam `olist_*_dataset.csv`.
- A relação entre CUSTOMERS e ORDERS é 1:1 por `customer_id` nesta base. A mesma pessoa pode fazer várias compras, identificadas por `customer_unique_id`.
- As linhas pontilhadas de geolocalização representam correspondências por prefixo de CEP, não FKs para uma chave única: há várias linhas por prefixo nos dois lados.
- `review_id` se repete; não foi marcado como PK. A chave única das avaliações não foi estabelecida.
- As chaves compostas de itens e pagamentos são propostas no modelo; sua unicidade não foi auditada. A integridade referencial completa também não foi auditada.

Ao juntar itens, pagamentos e avaliações por pedido, ou associar diretamente geolocalização, podem surgir múltiplas combinações de linhas. Agregue no nível da análise antes de calcular totais.
