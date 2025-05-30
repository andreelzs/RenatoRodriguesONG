from django.db import models
from django.conf import settings
# Importar o modelo Voluntario do app voluntarios
# É uma boa prática referenciar modelos de outros apps através de string 'app_label.ModelName'
# para evitar importações circulares, mas como Voluntario já deve estar definido,
# podemos importar diretamente se não houver problemas de ordem de carregamento.
# No entanto, para garantir, usaremos a string.
# from voluntarios.models import Voluntario -> Alternativa se não houver circularidade

class Tarefa(models.Model):
    STATUS_TAREFA = [
        ('PEND', 'Pendente'),
        ('FAZE', 'Sendo feita'),
        ('CONC', 'Concluída'),
        ('CANC', 'Cancelada'), # Adicionando um status de cancelada
    ]

    PRIORIDADE_TAREFA = [
        (1, 'Baixa'),
        (2, 'Média'),
        (3, 'Alta'),
        (4, 'Urgente'),
    ]

    titulo = models.CharField(max_length=200, verbose_name='Título da Tarefa')
    descricao = models.TextField(verbose_name='Descrição Detalhada')
    status = models.CharField(
        max_length=4,
        choices=STATUS_TAREFA,
        default='PEND',
        verbose_name='Status'
    )
    prioridade = models.IntegerField(
        choices=PRIORIDADE_TAREFA,
        default=2, # Média
        verbose_name='Prioridade'
    )
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    data_prevista_conclusao = models.DateField(blank=True, null=True, verbose_name='Prazo de Entrega')
    data_conclusao_efetiva = models.DateField(blank=True, null=True, verbose_name='Data de Conclusão Efetiva')
    
    voluntario_responsavel = models.ForeignKey(
        'voluntarios.Voluntario', # Usando string para evitar importação circular
        on_delete=models.SET_NULL, # Se o voluntário for excluído, a tarefa não é, mas fica sem responsável
        null=True,
        blank=True, # Uma tarefa pode ser criada sem um voluntário inicialmente
        related_name='tarefas_atribuidas',
        verbose_name='Voluntário Responsável'
    )
    
    atribuido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Usuário do sistema (Colaborador/Admin) que atribuiu
        on_delete=models.SET_NULL,
        null=True,
        blank=True, # Pode ser uma tarefa criada pelo próprio voluntário ou sistema
        related_name='tarefas_criadas',
        verbose_name='Atribuído Por'
    )
    
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações Adicionais')

    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
        ordering = ['-prioridade', 'data_prevista_conclusao', 'titulo'] # Ordenar por prioridade (maior primeiro), depois prazo

    def __str__(self):
        return f"{self.titulo} ({self.get_status_display()})"
