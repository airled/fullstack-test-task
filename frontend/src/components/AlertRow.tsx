import { Badge } from "react-bootstrap";
import { getLevelVariant, formatDate } from '../utils'
import type { AlertItem } from "../interfaces";

export default function AlertRow(alert: AlertItem) {
  return (
    <tr key={alert.id}>
      <td>{alert.id}</td>
      <td className="small">{alert.file_id}</td>
      <td>
        <Badge bg={getLevelVariant(alert.level)}>{alert.level}</Badge>
      </td>
      <td>{alert.message}</td>
      <td>{formatDate(alert.created_at)}</td>
    </tr>
  )
}
