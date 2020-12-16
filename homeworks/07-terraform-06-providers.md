# Домашнее задание к занятию "7.6. Написание собственных провайдеров для Terraform."

## Задача 1. 
Давайте потренируемся читать исходный код AWS провайдера, который можно склонировать от сюда: 
[https://github.com/hashicorp/terraform-provider-aws.git](https://github.com/hashicorp/terraform-provider-aws.git).
Просто найдите нужные ресурсы в исходном коде и ответы на вопросы станут понятны.  

1. Найдите, где перечислены все доступные `resource` и `data_source`, приложите ссылку на эти строки в коде на 
гитхабе.
```
Здесь resources: https://github.com/hashicorp/terraform-provider-aws/blob/1776cbf7cac4a821fcc3aebe06fc52845aab4e11/aws/provider.go#L167

Здесь data_sources: https://github.com/hashicorp/terraform-provider-aws/blob/1776cbf7cac4a821fcc3aebe06fc52845aab4e11/aws/provider.go#L394
```

2. Для создания очереди сообщений SQS используется ресурс `aws_sqs_queue` у которого есть параметр `name`. 
    * С каким другим параметром конфликтует `name`? Приложите строчку кода, в которой это указано.
    ```
    name_prefix
    
    https://github.com/hashicorp/terraform-provider-aws/blob/1776cbf7cac4a821fcc3aebe06fc52845aab4e11/aws/resource_aws_sqs_queue.go#L56
    ```
    * Какая максимальная длина имени? 
    ```
    80 символов
    
    https://github.com/hashicorp/terraform-provider-aws/blob/1776cbf7cac4a821fcc3aebe06fc52845aab4e11/aws/validators.go#L1031
    ```
    * Какому регулярному выражению должно подчиняться имя? 
    ```
    ^[0-9A-Za-z-_]+$
    
    https://github.com/hashicorp/terraform-provider-aws/blob/1776cbf7cac4a821fcc3aebe06fc52845aab4e11/aws/validators.go#L1035
    ```

## Задача 2. (Не обязательно) 
В рамках вебинара и презентации мы разобрали как создать свой собственный провайдер на примере кофемашины. 
Также вот официальная документация о создании провайдера: 
[https://learn.hashicorp.com/collections/terraform/providers](https://learn.hashicorp.com/collections/terraform/providers).

1. Проделайте все шаги создания провайдера.
2. В виде результата приложение ссылку на исходный код.
3. Попробуйте скомпилировать провайдер, если получится то приложите снимок экрана с командой и результатом компиляции.   
