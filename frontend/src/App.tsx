import AppRouter from "./routes/app-router";

const App = () => {
  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <AppRouter />
    </div>
  );
};

export default App;
