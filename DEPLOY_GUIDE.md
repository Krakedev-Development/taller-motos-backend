# Guía de Despliegue (AWS CLI)

Esta guía detalla el proceso para subir el backend a AWS utilizando únicamente el **AWS CLI**.

## 1. Requisitos Previos

- **AWS CLI Instalado**: Se instala con `winget install -e --id Amazon.AWSCLI`.
- **Credenciales Configuradas**: Ejecuta `aws configure` e ingresa tu **Access Key ID**, **Secret Access Key** y la región `us-east-1`.
- **Bucket de S3**: Ya contamos con uno creado por SAM: `aws-sam-cli-managed-default-samclisourcebucket-onon5eakfl9a`.

---

## 2. Proceso de Despliegue

Cada vez que realices cambios en el código, debes seguir estos dos pasos:

### Paso 1: Empaquetado (`Package`)
Este comando comprime las carpetas de las Lambdas, las sube a S3 y genera un archivo de configuración listo para AWS.

```powershell
aws cloudformation package `
  --template-file template.yml `
  --s3-bucket aws-sam-cli-managed-default-samclisourcebucket-onon5eakfl9a `
  --output-template-file deployment.yaml
```

### Paso 2: Despliegue (`Deploy`)
Este comando toma el archivo generado (`deployment.yaml`) y actualiza los recursos en Amazon.

```powershell
aws cloudformation deploy `
  --template-file deployment.yaml `
  --stack-name motorcycle-repair-shop `
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM `
  --s3-bucket aws-sam-cli-managed-default-samclisourcebucket-onon5eakfl9a `
  --parameter-overrides Environment="prod" DBUrl="https://toklwbqrgqsgaovzleev.supabase.co" DBKey="sb_publishable_9ToFd0mY6_QhXaGecuwxQA_ixnC9hQ0" LogRetentionDays="14"
```

---

## 3. ¿Qué es S3 y por qué es necesario?

**S3 (Simple Storage Service)** es el servicio de almacenamiento de archivos de Amazon.

### ¿Por qué lo usamos aquí?

1. **Limitación de Tamaño**: AWS no permite enviar archivos de configuración (`template.yml`) de más de **51KB** por texto. Como nuestro proyecto es grande, lo subimos a S3 para que AWS lo lea desde allí.
2. **Transferencia de Código**: Tu computadora zipea el código y lo guarda en S3. Las Lambdas en AWS leen su código directamente desde estos archivos en S3.

---

## 4. Solución de Problemas
Si el despliegue se "atasca" o da error de estado:
1. Borra el stack fallido: `aws cloudformation delete-stack --stack-name motorcycle-repair-shop`.
2. Espera a que Amazon limpie los recursos.
3. Vuelve a ejecutar los pasos de Package y Deploy.
