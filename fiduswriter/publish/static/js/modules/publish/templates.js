import {escapeText} from "../common"

export const submitDialogTemplate = ({messageToEditor}) =>
    `<h3>${gettext('Submission information')}</h3>
    <table class="fw-dialog-table fw-dialog-table-wide">
        <tbody>
            <tr>
                <th><h4 class="fw-tablerow-title">${gettext('Message to editor')}</h4></th>
                <td class="entry-field">
                    <textarea id="submission-message" rows="8" style="width:678px;resize:none;">${escapeText(messageToEditor)}</textarea>
                </td>
            </tr>
        </tbody>
    </table>`

export const publishDialogTemplate = ({messageToEditor}) =>
    `<h3>${gettext('Submission information')}</h3>
    <table class="fw-dialog-table fw-dialog-table-wide">
        <tbody>
            <tr>
                <th><h4 class="fw-tablerow-title">${gettext('Message from submitter')}</h4></th>
                <td>
                    ${escapeText(messageToEditor)}
                </td>
            </tr>
        </tbody>
    </table>`
