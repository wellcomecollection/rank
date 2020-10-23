import { NextPage } from "next";
type Props = {
  success: boolean;
};
const Index: NextPage<Props> = ({ success }) => {
  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        background: success ? "green" : "red",
        color: "white",
        fontSize: "50px",
        textAlign: "center",
        paddingTop: "25px",
      }}
    >
      {success ? "Success" : "Fail"}
    </div>
  );
};

Index.getInitialProps = async ({ res }) => {
  const resp = await fetch("http://localhost:3000/api/eval");
  const json = await resp.json();
  const success = json.success;

  return { success: success };
};

export default Index;
