import { Badge, Button } from "react-bootstrap";
import { formatDate, formatSize, getProcessingVariant } from "../utils";
import type { FileItem } from "../interfaces";

export default function FileRow(file: FileItem) {
  return (
    <tr key={file.id}>
      <td>
        <div className="fw-semibold">{file.title}</div>
        <div className="small text-secondary">{file.id}</div>
      </td>
      <td>{file.original_name}</td>
      <td>{file.mime_type}</td>
      <td>{formatSize(file.size)}</td>
      <td>
        <Badge bg={getProcessingVariant(file.processing_status)}>
          {file.processing_status}
        </Badge>
      </td>
      <td>
        <div className="d-flex flex-column gap-1">
          <Badge bg={file.requires_attention ? "warning" : "success"}>
            {file.scan_status ?? "pending"}
          </Badge>
          <span className="small text-secondary">
            {file.scan_details ?? "Ожидает обработки"}
          </span>
        </div>
      </td>
      <td>{formatDate(file.created_at)}</td>
      <td className="text-nowrap">
        <Button
          as="a"
          href={`http://localhost:8000/files/${file.id}/download`}
          variant="outline-primary"
          size="sm"
        >
          Скачать
        </Button>
      </td>
    </tr>
  )
}
