import {escapeText, localizeDate} from "../common"


const EVENT_TYPES = {
    'submit': gettext('Submitted'),
    'publish': gettext('Published'),
    'review': gettext('Reviewed'),
    'reject': gettext('Rejected')
}

const STATUS_TYPES = {
    'unknown': gettext('Unknown'),
    'submitted': gettext('Submitted'),
    'published': gettext('Published'),
    'rejected': gettext('Rejected'),
    'unsubmitted': gettext('Unsubmitted'),
    'resubmitted': gettext('Resubmitted')
}


const messageTr = ({messages}) => {
    if (!messages.length) {
        return ''
    }
    return `
    <tr>
        <th><h4 class="fw-tablerow-title">${gettext('Log')}</h4></th>
        <td>
            ${
    messages.slice().reverse().map(
        event =>
            `<div>
                <i>${localizeDate(event.time * 1000)}</i>
                &nbsp;
                <b>${EVENT_TYPES[event.type]}</b>
                &nbsp;${gettext('by')}&nbsp;
                ${event.user}
                ${event.message.length ? `:&nbsp;${escapeText(event.message)}` : ''}
            </div>`
    ).join('')
}
        </td>
    </tr>`
}

export const submitDialogTemplate = ({messages, status}) =>
    `<table class="fw-data-table fw-dialog-table fw-dialog-table-wide">
        <tbody>
        <tr>
            <th><h4 class="fw-tablerow-title">${gettext('Status')}</h4></th>
            <td><div class="fw-inline">${STATUS_TYPES[status]}</div></td>
        </tr>
            ${messageTr({messages})}
            <tr>
                <th><h4 class="fw-tablerow-title">${gettext('Message')}</h4></th>
                <td class="entry-field fw-inline">
                    <textarea id="submission-message" rows="8" style="resize:none;"></textarea>
                </td>
            </tr>
        </tbody>
    </table>`
