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

export const overviewBodyTemplate = ({_user, siteName, publications, authors, keywords, filters}) => `
    <div class="headers">
        <h1 class="site-name">${siteName}</h1>
    </div>
    <div class="content">
        <div class="filters">
            <div class="filter">
                <h3 class="filter-title">${gettext('Keywords')}</h3>
                <div class="keywords">
                    ${keywords.map((keyword, index) => `<span class="keyword${filters.keyword === keyword ? ' selected' : ''}" data-index="${index}">${escapeText(keyword)}</span>`).join('')}
                </div>
            </div>
            <div class="filter">
                <h3 class="filter-title">${gettext('Authors')}</h3>
                <div class="authors">
                    ${authors.map((author, index) => `<span class="author${filters.author === author ? ' selected' : ''}" data-index="${index}">${escapeText(author)}</span>`).join('')}
                </div>
            </div>
        </div>
        <div class="articles">${publications.map(publication => publicationOverviewTemplate(publication)).join('')}</div>
    </div>
    `

export const websiteOverviewTitle = gettext('Documents')
