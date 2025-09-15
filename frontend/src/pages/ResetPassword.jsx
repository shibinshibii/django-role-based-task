import api from "../api"
import { useSearchParams ,Navigate, useNavigate} from "react-router-dom"
import { ToastContainer,toast,Bounce } from "react-toastify"
import { useState } from "react"

function ResetPassword(){
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const uid = searchParams.get("uid")
    const token = searchParams.get("token")
    const [newPassword,setNewPassword] = useState("")
    const [confirmPassword,setConfirmPassword] = useState("")
      const [loading, setLoading] = useState(false);


    const handleSubmit = async(e) => {
        setLoading(true);
        e.preventDefault();

        try{
            const res = await api.post("/reset-password/",{newPassword,confirmPassword,uid,token})
            toast.success(res.data?.detail || "Password reset Successfull. Redirecting to Login...", {
        position: "bottom-center",
        autoClose: 5000,
        theme: "light",
        transition: Bounce,
      });
      setTimeout(() => {navigate('/login')},2500)

        } catch(error) {
            toast.error(
        error.response?.data?.detail || error.message || "Something went wrong",
        {
          position: "bottom-center",
          autoClose: 5000,
          theme: "light",
          transition: Bounce,
        }
      );

        }finally{
            setLoading(false)
        }
        

    }

    return <div>
        <form className="form-container" onSubmit={handleSubmit}>
        <h1>Reset Password</h1>
        <input
          className="form-input"
          type="password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          placeholder="New Password"
        />
        <input
          className="form-input"
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="Confirm Password"
        />
        <button type="submit" className="form-button" disabled={loading}>
          {loading ? "Resetting..." : "Reset"}
        </button>
      </form>
      <ToastContainer
        position="bottom-center"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick={false}
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
        transition={Bounce}
      />
    </div>

}
export default ResetPassword