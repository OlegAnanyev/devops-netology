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