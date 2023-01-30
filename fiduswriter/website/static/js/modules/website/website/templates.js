import {escapeText} from "../../common"

const publicationOverviewTemplate = ({title, keywords, authors, updated, _added, abstract, id}) =>
    `<a class="article"  href="/article/${id}/">
        <div class="keywords">${keywords.map(keyword => `<div class="keyword">${escapeText(keyword)}</div>`).join("")}</div>
        <h1 class="article-title">${title}</h1>
        <h3 class="article-updated">${updated.slice(0, 10)}</h3>
        <div class="authors">${authors.map(author => `<div class="author">${escapeText(author)}</div>`).join("")}</div>
        <div class="abstract">${abstract.slice(0, 250).split("\n").map(part => `<p>${escapeText(part)}</p>`).join("")}</div>
    </a>`

export const articleBodyTemplate = ({_user, publication}) =>
    `<link rel="stylesheet" href="${staticUrl("css/website_overview.css")}">
    ${publication.can_edit ? `<div class="edit"><a href="/document/${publication.doc_id}/">${gettext("Edit")}</a></div>` : ""}
        ${publication.content}`

export const overviewContentTemplate = ({keywords, authors, publications, filters}) =>
    `<div class="filters">
        <div class="filter">
            <h3 class="filter-title">${gettext("Keywords")}</h3>
            <div class="keywords">
                ${keywords.map((keyword, index) => `<span class="keyword${filters.keyword === keyword ? " selected" : ""}" data-index="${index}">${escapeText(keyword)}</span>`).join("")}
            </div>
        </div>
        <div class="filter">
            <h3 class="filter-title">${gettext("Authors")}</h3>
            <div class="authors">
                ${authors.map((author, index) => `<span class="author${filters.author === author ? " selected" : ""}" data-index="${index}">${escapeText(author)}</span>`).join("")}
            </div>
        </div>
    </div>
    <div class="articles">${publications.map(publication => publicationOverviewTemplate(publication)).join("")}</div>`

export const overviewBodyTemplate = ({user, siteName, publications, authors, keywords, filters}) => `
    <link rel="stylesheet" href="${staticUrl("css/website_overview.css")}">
    <div class="headers">
        ${user.is_authenticated ? `<div class="breadcrumbs"><a href="/documents/">${gettext("Documents")}</a></div>` : ""}
        <h1 class="site-name">${siteName}</h1>
    </div>
    <div class="content">
        ${overviewContentTemplate({keywords, authors, publications, filters})}
    </div>
    `

export const websiteOverviewTitle = gettext("Documents")
