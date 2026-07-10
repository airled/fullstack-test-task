import {Badge, Card, Spinner, Table} from "react-bootstrap";
import type { FileListProps } from "../interfaces";
import FileRow from './FileRow'


export default function FileList({ files, isLoading }: FileListProps ) {
  return (<Card className="shadow-sm border-0 mb-4">
    <Card.Header className="bg-white border-0 pt-4 px-4">
      <div className="d-flex justify-content-between align-items-center">
        <h2 className="h5 mb-0">Файлы</h2>
        <Badge bg="secondary">{files.length}</Badge>
      </div>
    </Card.Header>
    <Card.Body className="px-4 pb-4">
      {isLoading ? (
        <div className="d-flex justify-content-center py-5">
          <Spinner animation="border" />
        </div>
      ) : (
        <div className="table-responsive">
          <Table hover bordered className="align-middle mb-0">
            <thead className="table-light">
              <tr>
                <th>Название</th>
                <th>Файл</th>
                <th>MIME</th>
                <th>Размер</th>
                <th>Статус</th>
                <th>Проверка</th>
                <th>Создан</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {files.length === 0 ? (
                <tr>
                  <td colSpan={8} className="text-center py-4 text-secondary">
                    Файлы пока не загружены
                  </td>
                </tr>
              ) : (
                files.map(FileRow)
              )}
            </tbody>
          </Table>
        </div>
      )}
    </Card.Body>
  </Card>)
}
