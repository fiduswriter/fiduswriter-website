const publicationOverviewTemplate = ({title, _content, id}) =>
    `<li><a href="/article/${id}/">${title}</a></li>`

export const articleBodyTemplate = ({_user, publication}) =>
    `${publication.content}`

export const overviewBodyTemplate = ({_user, publications}) =>
    `<ul>${publications.map(publication => publicationOverviewTemplate(publication)).join('')}</ul>`

export const websiteOverviewTitle = gettext('Documents')
