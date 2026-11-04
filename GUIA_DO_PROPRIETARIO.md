# Huerlem Apps: guia do proprietário

Estado: **pré-visualização, não publicar.**
- `site.json` tem `"indexing": false`, por isso todas as páginas levam `noindex` e o `robots.txt` bloqueia motores de busca.
- `python3 tools/validate.py --release` falha até estarem preenchidos os dados abaixo e resolvida a revisão jurídica.

## 1. Dados do proprietário em falta

Estes dados ficam **públicos** no site e dentro do app. Os documentos legais do app usam os mesmos valores.

| Dado | Onde aparece | `site.json` | `Config/Owner.xcconfig` (ElectionMagica) |
|---|---|---|---|
| Nome legal (pessoa ou empresa) | Rodapé; Privacidade (responsável pelo tratamento); Termos | `owner.legal_name` | `EM_OWNER_LEGAL_NAME` |
| Morada postal | Privacidade; Termos | `owner.postal_address` | `EM_OWNER_POSTAL_ADDRESS` |
| E-mail de contacto e suporte | Rodapé; Suporte; todos os documentos | `owner.contact_email` (ou `support_email` em `app.json`, se quiser um e-mail só para o app) | `EM_SUPPORT_EMAIL` |
| Lei aplicável | Termos; Privacidade | `owner.governing_law` | `EM_GOVERNING_LAW` |
| Endereço do site | Todos os URLs | `base_url` (e `cname`, se usar domínio próprio) | `EM_WEBSITE_URL` (§3) |

Notas:
- A morada fica visível para qualquer pessoa. Se for trader na UE (DSA), a Apple também a mostra na App Store.
- Recomendo um e-mail dedicado ao suporte, que possa manter durante anos.
- A redação da lei aplicável (por exemplo, «the laws of England and Wales») deve ser confirmada na revisão jurídica.

## 2. Revisão jurídica pendente (17 notas)

As notas «LEGAL REVIEW REQUIRED» estão nos documentos do **app** (`ElectionMagica/LEGAL/*.md`). Aparecem **dentro do app** e no site, destacadas a amarelo na pré-visualização.

| Documento | Nota | EN | PT-BR | ES |
|---|---|---|---|---|
| Privacy Policy §10 | Identidade do responsável, bases legais, representante | ✓ | ✓ | ✓ |
| Terms §idade | Alinhar os 18+ com a classificação etária do App Store Connect | ✓ | ✓ | ✓ |
| Terms, responsabilidade | Exceções da lei do consumidor por jurisdição | ✓ | ✓ | ✓ |
| Terms, lei aplicável | Lei e foro | ✓ | ✓ | ✓ |
| Data Retention, registo de consultas | Registo que sobrevive a «Apagar dados locais» | ✓ | ✓ | ✓ |
| Subscription Terms, reembolsos | Direito de arrependimento (CDC / desistimiento) | — | ✓ | ✓ |

Como resolver:
1. A revisão jurídica decide o texto final de cada nota.
2. O texto é alterado em `ElectionMagica/LEGAL/` (o app e o site usam os mesmos ficheiros).
3. A nota «LEGAL REVIEW REQUIRED» é removida.
4. Corre-se `tools/sync_election_magick_legal.py` neste repositório.

O site nunca tem uma versão diferente da do app.

## 3. URLs finais

Recomendação: repositório **`huerlemp2-cloud.github.io`**, que fica na raiz do domínio GitHub Pages da conta.

| Uso | URL |
|---|---|
| `EM_WEBSITE_URL` | `https://huerlemp2-cloud.github.io/election-magick` |
| No `Owner.xcconfig` (o xcconfig trata `//` como comentário) | `EM_WEBSITE_URL = https:/$()/huerlemp2-cloud.github.io/election-magick` |
| App Store Connect → Privacy Policy URL (en-GB) | `https://huerlemp2-cloud.github.io/election-magick/en/privacy/` |
| App Store Connect → Support URL (en-GB) | `https://huerlemp2-cloud.github.io/election-magick/en/support/` |
| pt-BR | `…/election-magick/pt-br/privacy/` e `…/election-magick/pt-br/support/` |
| es-ES | `…/election-magick/es/privacy/` e `…/election-magick/es/support/` |
| Termos (opcional, campo de EULA ou descrição) | `…/election-magick/en/terms/` |
| Página do app (Marketing URL, opcional) | `https://huerlemp2-cloud.github.io/election-magick/` |

O app abre `EM_WEBSITE_URL/<en|pt-br|es>/support`. O GitHub Pages redireciona para `…/support/`, por isso estes endereços funcionam sem alterar o app.

**Alternativa:** um repositório com outro nome, por exemplo `huerlem-apps`. Nesse caso, todos os URLs ganham o prefixo `/huerlem-apps`: `https://huerlemp2-cloud.github.io/huerlem-apps/election-magick`.

**Domínio próprio, mais tarde:**
1. Adicione `"cname": "<domínio>"` em `site.json` e configure o DNS.
2. O GitHub redireciona os endereços `github.io` antigos para o domínio novo, por isso os links já gravados no app continuam a funcionar.
3. Na versão seguinte do app, atualize o `EM_WEBSITE_URL`.

Os ficheiros `APPSTORE/*/privacy_policy_url.txt` e `support_url.txt` do ElectionMagica usam `[[WEBSITE_URL]]/<lang>/…`. Com o valor acima, dão exatamente estes URLs.

## 4. Publicar no GitHub Pages (só no navegador, sem instalar nada)

1. **Criar o repositório.**
   - Em <https://github.com/new>: Owner `huerlemp2-cloud`, nome `huerlemp2-cloud.github.io`, **Private**, sem README.
   - **Create repository**.
   - Avise-me: eu envio este conteúdo para lá. O repositório fica privado enquanto revê.
2. **Rever.** Veja a pré-visualização e o repositório.
3. **Dados e revisão.** Envie-me os dados de §1 e o texto final da revisão jurídica. Eu:
   - preencho o `site.json`;
   - mudo `"indexing"` para `true`;
   - sincronizo os documentos;
   - corro `tools/build.py` e `tools/validate.py --release`, que tem de dar **PASS**;
   - envio para o repositório.
4. **Tornar público.** Settings → General → Danger Zone → **Change visibility → Public**. O GitHub Pages gratuito exige um repositório público. Antes disso, confirme que o repositório só tem o site.
5. **Ativar o Pages.**
   - Settings → **Pages** → Build and deployment → Source **Deploy from a branch**.
   - Branch `main`, pasta **`/docs`** → **Save**.
   - Ao fim de 1–2 minutos aparece o endereço. Marque **Enforce HTTPS**.
6. **Verificar.** Abra os URLs de §3 no iPhone e no PC, incluindo as versões pt-br e es.
7. **App Store Connect e app.**
   - Cole os URLs de privacidade e de suporte em cada localização.
   - No ElectionMagica, preencha o `Owner.xcconfig` com os mesmos valores (eu faço isto num commit à parte, sem builds).

Não é usado GitHub Actions: o site já gerado está em `docs/` e o Pages serve-o tal como está.

## 5. Manutenção

- **Alterar texto, ou adicionar uma app ou screenshots:** ver `README.md`. Depois de cada alteração, correr `tools/build.py` e `tools/validate.py`.
- **Screenshots:** só capturas reais da versão de produção (TestFlight ou App Store), nunca da versão de teste QA. Enquanto a lista estiver vazia, a secção não aparece.
- **IntelliShop e Dream Tales:** aparecem como «In development», sem descrição, funcionalidades, preços, datas nem políticas. Cada uma ganha a sua página de privacidade, termos e suporte quando os documentos estiverem aprovados (`content/apps/<app>/legal/README.md`).
