# devops-netology
# by Oleg Ananyev

Согласно файлу .gitignore, расположенному в поддиректории /terraform/, будут игнорироваться git-ом следующие файлы:

- все файлы в поддиректории /.terraform/
- файлы с расширением *.tfstate и с любым расширением, добавленным после этого, например файл 123.tfstate.bak
- файлы с именем crash.log, override.tf, override.tf.json
- файлы, имеющие в своём имени "_override.tf", "_override.tf.json"
- а также файлы с именами .terraformrc и terraform.rc
---------------------
Новая строка в README

Ещё одна новая строка.

New line from "fix" branch

Some new lines from PyCharm:
----------------------------------------------------
- line
- line
- line

Эта строка добавлена в README в рамках специальной ветки, для рефакторинга данного файла.

Эта строка попадёт в ветку master путём rebase...

Эта строка была создана в ветке experiment, но тоже попадёт в  master благодаря rebase...
