import type FileItem from "./FileItem";

export default interface FileListProps {
  files: FileItem[],
  isLoading: boolean,
}
