export default function Badge({ type, value }) {
  if (!value) return null;
  return <span className={`badge badge-${type}-${value}`}>{value.replace("_", " ")}</span>;
}
