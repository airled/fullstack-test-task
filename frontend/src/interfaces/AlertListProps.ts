import type AlertItem from "./AlertItem"

export default interface AlertListProps {
  alerts: AlertItem[],
  isLoading: boolean,
}
