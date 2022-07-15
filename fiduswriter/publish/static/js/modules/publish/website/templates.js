import {escapeText} from "../../common"

const publicationOverviewTemplate = ({title, keywords, authors, updated, _added, id}) =>
    `<a class="article"  href="/article/${id}/">
        <div class="keywords">${keywords.map(keyword => `<div class="keyword">${escapeText(keyword)}</div>`).join('')}</div>
        <h1 class="article-title">${title}</h1>
        <h3 class="article-updated">${updated.slice(0, 10)}</h3>
        <div class="authors">${authors.map(author => `<div class="author">${escapeText(author)}</div>`).join('')}</div>
    </a>`

export const articleBodyTemplate = ({_user, publication}) =>
    `${publication.can_edit ? `<div class="edit"><a href="/document/${publication.doc_id}/">${gettext("Edit")}</a></div>` : ''}
        ${publication.content}`

export const overviewBodyTemplate = ({_user, publications}) =>
    `<div class="articles">${publications.map(publication => publicationOverviewTemplate(publication)).join('')}</div>`

export const websiteOverviewTitle = gettext('Documents')
