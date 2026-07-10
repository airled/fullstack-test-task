"use client";

import { FormEvent, useEffect, useState } from "react";
import {
  Alert,
  Button,
  Card,
  Col,
  Container,
  Row,
} from "react-bootstrap";
import { FileList, AlertList, FileUploadModal } from "../components";
import type { FileItem, AlertItem } from '../interfaces';

export default function Page() {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [title, setTitle] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function loadData() {
    setIsLoading(true);
    setErrorMessage(null);

    try {
      const [
        filesResponse,
        alertsResponse,
      ] = await Promise.all([
        fetch(`http://localhost:8000/files`, { cache: "no-store" }),
        fetch(`http://localhost:8000/alerts`, { cache: "no-store" }),
      ]);

      if (!filesResponse.ok || !alertsResponse.ok) {
        throw new Error("Не удалось загрузить данные");
      }

      const [filesData, alertsData] = await Promise.all([
        filesResponse.json() as Promise<FileItem[]>,
        alertsResponse.json() as Promise<AlertItem[]>,
      ]);

      setFiles(filesData);
      setAlerts(alertsData);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Произошла ошибка");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    void loadData();
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!title.trim() || !selectedFile) {
      setErrorMessage("Укажите название и выберите файл");
      return;
    }

    setIsSubmitting(true);
    setErrorMessage(null);

    const formData = new FormData();
    formData.append("title", title.trim());
    formData.append("file", selectedFile);

    try {
      const response = await fetch(`http://localhost:8000/files`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Не удалось загрузить файл");
      }

      setShowModal(false);
      setTitle("");
      setSelectedFile(null);
      await loadData();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Произошла ошибка");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <Container fluid className="py-4 px-4 bg-light min-vh-100">
      <Row className="justify-content-center">
        <Col xxl={10} xl={11}>
          <Card className="shadow-sm border-0 mb-4">
            <Card.Body className="p-4">
              <div className="d-flex justify-content-between align-items-start gap-3 flex-wrap">
                <div>
                  <h1 className="h3 mb-2">Управление файлами</h1>
                  <p className="text-secondary mb-0">
                    Загрузка файлов, просмотр статусов обработки и ленты алертов.
                  </p>
                </div>
                <div className="d-flex gap-2">
                  <Button variant="outline-secondary" onClick={() => void loadData()}>
                    Обновить
                  </Button>
                  <Button variant="primary" onClick={() => setShowModal(true)}>
                    Добавить файл
                  </Button>
                </div>
              </div>
            </Card.Body>
          </Card>

          {errorMessage ? (
            <Alert variant="danger" className="shadow-sm">
              {errorMessage}
            </Alert>
          ) : null}

          <FileList files={files} isLoading={isLoading} />
          <AlertList alerts={alerts} isLoading={ isLoading} />
          <FileUploadModal
            showModal={showModal}
            setShowModal={setShowModal}
            handleSubmit={handleSubmit}
            isSubmitting={isSubmitting}
            title={title}
            setTitle={setTitle}
            setSelectedFile={setSelectedFile}
          />
        </Col>
      </Row>
    </Container>
  );
}
