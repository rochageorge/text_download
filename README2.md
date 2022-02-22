## Solução
* Para realização do teste, foram utilizadas as bibliotecas `jsonpath_ng` e `datetime` como mostra abaixo.
> #### from jsonpath_ng import jsonpath, parse
> #### from datetime import date
* A biblioteca jsonpath_ng permite realizar a retirada de atributos de arquivos json de maneira simplificada.
* O datetime fora utilizado para facilitar a comparação entre as datas de inicio e fim de período desejado.

* O assert foi utilzado para garantir que as datas não estejam no futuro e que não sejam definidas antes de `1970`, como pode ser visto abaixo:
> #### assert today >= start_date, "Dates can't be in the future." 
> ####  assert start_date.year >= 1970, "Dates can't be before 1970." 


### Foram utilizadas as funções disponibilizadas:

* Para implementação das funções `get_year_journals`, `get_month_journals` e `get_day_journals` utilizaram a função disponivel:

> #### request_journals 


* Para implementação das funções  `download_all` utilizou-se a função disponivel:

> #### download_mutiple_jornals

## Execução:

* Todas as funções estão funcionando e gerando saida de acordo com o que foi descrito em cada função.
