import {escapeText} from "../../common"

const publicationOverviewTemplate = ({title, keywords, authors, updated, _added, abstract, id}) =>
    `<a class="article"  href="/article/${id}/">
        <div class="keywords">${keywords.map(keyword => `<div class="keyword">${escapeText(keyword)}</div>`).join("")}</div>
        <h1 class="article-title">${escapeText(title)}</h1>
        <h3 class="article-updated">${updated.slice(0, 10)}</h3>
        <div class="authors">${authors.map(author => `<div class="author">${escapeText(author)}</div>`).join("")}</div>
        <div class="abstract">${abstract.slice(0, 250).split("\n").map(part => `<p>${escapeText(part)}</p>`).join("")}</div>
    </a>`

export const articleBodyTemplate = ({_user, publication, siteName}) =>
    `<link rel="stylesheet" href="${staticUrl("css/website.css")}">
        <nav class="header">
            <a href="/">${
    escapeText(siteName)
}</a>
            <span>${
    escapeText(publication.title)
}</span>
            ${
    publication.can_edit ? `<a href="/document/${publication.doc_id}/">${gettext("Edit")}</a>` : ""
}
        </nav>
        <div class="articles">
            <div class="keywords">${publication.keywords.map(keyword => `<span class="keyword">${escapeText(keyword)}</div>`).join("")}</span>
            <h1 class="article-title">${escapeText(publication.title)}</h1>
            <h3 class="article-updated">${publication.updated.slice(0, 10)}</h3>
            ${publication.content}
        </div>`

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
    <link rel="stylesheet" href="${staticUrl("css/website.css")}">
    <div class="headers">
        ${user.is_authenticated ? `<nav class="header"><a href="/documents/">${gettext("Fidus Writer")}</a></nav>` : ""}
        <h1 class="site-name">${escapeText(siteName)}</h1>
    </div>
    <div class="content">
        ${overviewContentTemplate({keywords, authors, publications, filters})}
    </div>
    `
