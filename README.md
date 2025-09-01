# EduGestão - Sistema de Gestão Escolar

## 📋 Descrição

O EduGestão é um sistema completo de gestão escolar desenvolvido em Python com interface gráfica usando Flet. O sistema permite gerenciar alunos, professores, turmas, disciplinas, notas, frequência, comunicados e calendário escolar.

## 🚀 Funcionalidades

### 👥 Gestão de Usuários
- **Administrador**: Acesso completo ao sistema
- **Secretaria**: Gestão de matrículas e documentos
- **Professor**: Gestão de notas e frequência
- **Aluno**: Visualização de notas e frequência
- **Responsável**: Acompanhamento do aluno
- **Suporte**: Logs e configurações

### 📊 Módulos Principais
- **Dashboard**: Visão geral com métricas
- **Alunos**: Cadastro e gestão de estudantes
- **Professores**: Cadastro e gestão de docentes
- **Turmas**: Organização de classes
- **Disciplinas**: Gestão de matérias
- **Notas**: Lançamento e consulta de notas
- **Frequência**: Controle de presença
- **Comunicados**: Sistema de mensagens
- **Calendário**: Eventos escolares

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Flet** - Framework para interface gráfica
- **SQLite** - Banco de dados
- **SQLAlchemy** - ORM (opcional)

## 📦 Instalação

### Pré-requisitos
```bash
python --version  # Python 3.8 ou superior
pip --version     # Gerenciador de pacotes Python
```

### Instalação das Dependências
```bash
pip install flet
```

### Execução
```bash
python main.py
```

## 🔐 Credenciais de Acesso

| Usuário | Senha | Papel |
|---------|-------|-------|
| admin | admin123 | Administrador |
| secretaria | sec123 | Secretaria |
| prof | prof123 | Professor |
| aluno | aluno123 | Aluno |
| responsavel | resp123 | Responsável |
| suporte | sup123 | Suporte |

## 📁 Estrutura do Projeto

```
sistema_escolar/
├── main.py                 # Arquivo principal
├── config.py              # Configurações do sistema
├── sistema_escolar.db     # Banco de dados SQLite
├── models/                # Modelos de dados
│   ├── aluno.py
│   ├── professor.py
│   ├── turma.py
│   └── ...
├── services/              # Lógica de negócio
│   ├── db.py
│   ├── aluno_service.py
│   ├── professor_service.py
│   └── ...
├── view/                  # Interfaces de usuário
│   ├── dashboard_view.py
│   ├── aluno_view.py
│   ├── professor_view.py
│   └── ...
└── UI/                    # Componentes de interface
    ├── login.py
    ├── shell.py
    └── ...
```

## 🎯 Melhorias Implementadas

### ✅ Funcionalidades Adicionadas
1. **Views Funcionais**: Implementação completa das interfaces
2. **Dashboard Interativo**: Métricas e estatísticas em tempo real
3. **Sistema de Navegação**: Menu dinâmico baseado no papel do usuário
4. **Gestão de Comunicados**: Sistema de mensagens
5. **Validação de Dados**: Regras de validação centralizadas
6. **Configuração Centralizada**: Arquivo de configurações

### 🔧 Melhorias Técnicas
1. **Arquitetura Modular**: Separação clara entre modelos, serviços e views
2. **Tratamento de Erros**: Mensagens de erro amigáveis
3. **Interface Responsiva**: Design adaptável
4. **Documentação**: README completo e comentários no código

## 🚧 Próximas Melhorias

### 📋 Funcionalidades Pendentes
- [ ] Implementação de todas as views restantes
- [ ] Sistema de backup automático
- [ ] Relatórios em PDF
- [ ] Sistema de notificações
- [ ] Integração com APIs externas
- [ ] Sistema de auditoria
- [ ] Backup na nuvem

### 🔧 Melhorias Técnicas
- [ ] Testes automatizados
- [ ] Logs detalhados
- [ ] Cache de dados
- [ ] Otimização de performance
- [ ] Interface mobile
- [ ] API REST

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Desenvolvimento

### Executar em Modo Desenvolvimento
```bash
# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Executar com debug
python main.py --debug
```

### Estrutura de Desenvolvimento
- **models/**: Definição das entidades do sistema
- **services/**: Lógica de negócio e acesso a dados
- **view/**: Interfaces de usuário
- **UI/**: Componentes reutilizáveis

## 📞 Suporte

Para dúvidas ou suporte, entre em contato através de:
- Email: suporte@edugestao.com
- Issues: GitHub Issues
- Documentação: Wiki do projeto

---

**EduGestão** - Transformando a gestão escolar com tecnologia moderna! 🎓
