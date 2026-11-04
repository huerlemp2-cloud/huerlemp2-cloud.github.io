# Política de Privacidade

Versão 1.0 · Vigência a partir de 2026-11-01

Esta Política de Privacidade explica como o app Election Magick ("o app") trata informações. O app é fornecido por [[OWNER_LEGAL_NAME]], [[OWNER_POSTAL_ADDRESS]] ("nós"). Contato: [[SUPPORT_EMAIL]].

Em resumo: o app funciona no seu aparelho. Não operamos servidores, não há contas de usuário e não recebemos seus dados astrológicos, sua localização nem as descrições dos seus rituais. Alguns recursos usam serviços da Apple, descritos abaixo.

## 1. Os cálculos são feitos no seu aparelho

<!-- fact:P-CALC-1 -->
Todos os cálculos astronômicos e astrológicos (posições planetárias, casas, horas planetárias, verificações de risco, classificações e rankings) são feitos no seu aparelho. Nenhum dado de entrada ou resultado de cálculo é enviado para nós. Não operamos nenhum servidor para o app.

## 2. Localização

<!-- fact:P-LOC-1 -->
Usar sua localização é opcional. O app só pede permissão depois de explicar o motivo, apenas "durante o uso do app" e apenas com precisão aproximada (cerca de 1 km). Você sempre pode escolher uma cidade; todos os recursos funcionam sem acesso à localização.

<!-- fact:P-LOC-2 -->
Se você escolher "Usar Localização Atual", o app obtém uma posição nova a cada cálculo. Para encontrar o nome do local e o fuso horário, suas coordenadas são enviadas ao serviço de geocodificação da Apple (Apple Maps). O app não guarda posições obtidas dessa forma, a menos que você salve o local.

<!-- fact:P-LOC-3 -->
Ao buscar uma cidade, o texto digitado é enviado ao Apple Maps para mostrar sugestões. A cidade escolhida (nome, país, coordenadas e fuso horário) é guardada no seu aparelho para que você possa reutilizá-la.

O tratamento das solicitações do Maps pela Apple está descrito na política de privacidade da Apple: https://www.apple.com/br/legal/privacy/

## 3. Informações guardadas no seu aparelho

<!-- fact:P-DATA-1 -->
Eleições salvas, locais salvos, entidades favoritas, perfis de ritual e o histórico de cálculos ficam guardados apenas no seu aparelho. Eles podem incluir a descrição do ritual que você digitou, a entidade escolhida, as coordenadas, o nome e o fuso horário do local e as datas calculadas.

<!-- fact:P-DATA-2 -->
Suas preferências (idioma, sistema de casas, nodo lunar, explicações por IA ativadas ou não) ficam guardadas no seu aparelho.

<!-- fact:P-DATA-3 -->
Quando você aceita os Termos de Uso e declara ter lido esta Política de Privacidade, o app registra no seu aparelho quais versões você aceitou, quando, e a versão do app.

## 4. Assinaturas e compras

<!-- fact:P-SUB-1 -->
As assinaturas são vendidas, cobradas, renovadas, canceladas e reembolsadas pela Apple, na App Store. A Apple processa seus dados de pagamento; nós nunca os vemos. O app recebe da Apple apenas as informações de transação verificadas necessárias para liberar o seu plano: o produto, as datas de compra e de expiração, os identificadores da transação e o estado da renovação.

<!-- fact:P-SUB-2 -->
Cada plano inclui um número de consultas por período. Para contá-las, o app guarda nas Chaves (Keychain) do seu aparelho (somente neste aparelho) um registro por período de assinatura formado por resumos criptográficos irreversíveis (SHA-256) das consultas já usadas. Esses resumos não contêm o texto do seu ritual, o local nem as datas de forma legível. Esse registro é mantido quando você usa "Apagar dados locais", para que a franquia não possa ser reiniciada, e, por causa do funcionamento do iOS, pode permanecer nas Chaves depois que você apaga o app.

## 5. Explicações por IA

<!-- fact:P-AI-1 -->
A IA nunca faz cálculos astrológicos e nunca altera um resultado. Ela apenas escreve explicações de resultados que o app já calculou.

<!-- fact:P-AI-2 -->
Por padrão, as explicações são escritas pela Apple Intelligence no seu aparelho (modelos Apple Foundation Models). Nada é enviado para fora do aparelho para isso. Você pode desativá-las em Ajustes → Explicações; o app passa então a mostrar uma explicação padrão gerada por ele mesmo.

<!-- fact:P-AI-3 -->
O Private Cloud Compute vem desativado. Ele só é usado se você o ativar em Ajustes → Explicações → Private Cloud Compute e confirmar a tela de informações mostrada antes da ativação.

<!-- fact:P-AI-7 -->
Mesmo ativado, o Private Cloud Compute é usado apenas para textos Premium mais longos. Explicações curtas continuam no seu aparelho.

<!-- fact:P-AI-4 -->
Quando o Private Cloud Compute é usado, o app envia um resumo compacto da carta já calculada: a data e a hora locais da eleição com o deslocamento UTC, a categoria da intenção e o tipo de operação, posições e casas do significador e da Lua, pontuações de dignidade, dia e hora planetários, status de risco e riscos apontados, condição da Lua, avaliação do operador, as principais razões do resultado e a classificação que o seu plano pode mostrar. O identificador da entidade escolhida e o nível de compatibilidade só são incluídos quando o texto pedido explica essa compatibilidade.

<!-- fact:P-AI-5 -->
Nunca são enviados ao Private Cloud Compute: coordenadas, nome do local, nome do fuso horário, a descrição do ritual que você digitou, anotações e qualquer identificador de conta ou de aparelho.

<!-- fact:P-AI-6 -->
A Apple processa as solicitações do Private Cloud Compute em servidores da Apple projetados para privacidade; a Apple declara que os dados são usados apenas para atender à solicitação e não são armazenados nem ficam acessíveis à Apple. Veja https://security.apple.com/blog/private-cloud-compute/ e a política de privacidade da Apple.

<!-- fact:P-AI-8 -->
Seu consentimento ao Private Cloud Compute é registrado no seu aparelho com a versão da tela de informações que você confirmou e a data e hora. Desativar o Private Cloud Compute apaga esse registro e interrompe o uso imediatamente. Se mudarmos as informações de forma relevante, o app pede o consentimento de novo.

<!-- fact:P-AI-9 -->
Nenhum recurso depende do Private Cloud Compute. Se ele estiver desativado ou indisponível (por exemplo, sem conexão, após o limite diário da Apple ou em aparelhos ou regiões não compatíveis), as explicações vêm da Apple Intelligence no seu aparelho ou da explicação padrão do app.

<!-- fact:P-AI-10 -->
O app não usa nenhum outro provedor de IA e não contém chaves de serviços de IA.

## 6. Relatórios que você exporta

<!-- fact:P-EX-1 -->
Os relatórios (PDF, texto ou arquivo de dados do Election Magick) são criados no seu aparelho somente quando você pede. Eles só saem do aparelho se você mesmo os compartilhar ou salvar pela folha de compartilhamento do iOS; a partir daí, o serviço que você escolher (por exemplo, e-mail ou nuvem) os trata segundo os próprios termos.

<!-- fact:P-EX-2 -->
Os relatórios em PDF e texto contêm a eleição calculada, o nome do local, o fuso horário e a descrição do ritual que você digitou, mas não as coordenadas do local.

<!-- fact:P-EX-3 -->
O arquivo de dados do Election Magick (.emreport) contém também as entradas necessárias para reproduzir o cálculo, incluindo as coordenadas do local. Compartilhe-o apenas com quem você queira que tenha essa informação.

<!-- fact:P-EX-4 -->
As cópias temporárias criadas para compartilhamento são protegidas pela proteção de arquivos do iOS e apagadas após uma hora.

## 7. Conexões de rede, diagnósticos e publicidade

<!-- fact:P-NET-1 -->
O próprio app se conecta somente a serviços da Apple: a App Store (assinaturas), o Apple Maps (busca de cidades e nomes de locais) e, se você ativar, o Private Cloud Compute. Os links que você toca (e-mail de suporte, nosso site, o contrato de licença da Apple, gerenciamento de assinatura, pedidos de reembolso) abrem fora do app.

<!-- fact:P-DIAG-1 -->
O app não contém software de análise, de relatórios de falhas nem de publicidade. Se você ativou "Compartilhar com Desenvolvedores" nos Ajustes do iOS, a Apple pode compartilhar conosco relatórios de falhas e estatísticas de uso conforme ela descreve; você pode desativar isso em Ajustes → Privacidade e Segurança → Análise e Melhorias.

<!-- fact:P-ADS-1 -->
Não exibimos publicidade, não rastreamos você em outros apps ou sites, não vendemos nem compartilhamos dados pessoais, e não há conta a criar.

## 8. Guarda e exclusão das suas informações

<!-- fact:P-RET-1 -->
Suas informações ficam no seu aparelho até que você as apague. Não guardamos nenhuma cópia. As cópias temporárias de exportação são apagadas após uma hora.

<!-- fact:P-DEL-1 -->
Ajustes → Apagar dados locais remove eleições salvas, locais, favoritos, perfis de ritual, histórico, o local escolhido, o registro do seu aceite jurídico, o estado da introdução e o seu consentimento ao Private Cloud Compute. Os resumos de consultas descritos na seção 4 permanecem. Apagar o app remove os dados dele do seu aparelho, exceto itens que o iOS mantém nas Chaves.

Mais detalhes: Política de Retenção de Dados (no app, em Ajustes → Jurídico).

## 9. Crianças

<!-- fact:P-KIDS-1 -->
O app não é direcionado a crianças nem foi projetado para uso por crianças.

## 10. Seus direitos

<!-- fact:P-RIGHTS-1 -->
Dependendo de onde você mora (por exemplo, pela LGPD no Brasil, pelo UK GDPR ou pelo GDPR da UE), você pode ter direitos de acesso, correção, eliminação e portabilidade dos seus dados pessoais e de oposição ao seu uso. Como não mantemos seus dados pessoais, você exerce esses direitos diretamente no app (ver, exportar ou apagar seus dados como descrito acima). Para dúvidas ou reclamações, escreva para [[SUPPORT_EMAIL]]. Você também pode reclamar a uma autoridade de proteção de dados, como a Autoridade Nacional de Proteção de Dados (ANPD), o Information Commissioner's Office (Reino Unido) ou a autoridade do seu país da UE/EEE.

LEGAL REVIEW REQUIRED: confirmar a identidade do controlador, as bases legais e eventuais exigências de encarregado/representante na jurisdição do titular do app ([[GOVERNING_LAW]]).

## 11. Alterações

Se alterarmos esta política de forma relevante, o app mostra a nova versão e pede que você a reconheça antes de continuar. A versão e a data de vigência aparecem no topo.
