# Django Ecommerce Project

A Django-based e-commerce web application.

## Make installation

Go to windows powershell as administrator and follow the steps:
1. Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
2. choco install make

## Project Installation

1. Clone the repository: `git clone https://github.com/dinesh1299/E-Commerce-Website-Using-Django-Framework.git`
2. Navigate to the project directory: `cd E-Commerce-Website-Using-Django-Framework`

## Initial setup
1. Go to settings.py in Ecommerce then change DATABASES - HOST: #your ip address
2. make deploy
   
## Usage

To run the development server:
1. make start

To stop the development server
1. make stop

