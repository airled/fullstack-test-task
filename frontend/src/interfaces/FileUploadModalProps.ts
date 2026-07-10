import { Dispatch, FormEvent, SetStateAction } from "react";

export default interface FileUploadModalProps {
  showModal: boolean,
  setShowModal: Dispatch<SetStateAction<boolean>>,
  handleSubmit: (event: FormEvent<HTMLFormElement>) => Promise<void>,
  isSubmitting: boolean,
  title: string,
  setTitle: Dispatch<SetStateAction<string>>,
  setSelectedFile: Dispatch<SetStateAction<File>>
}
