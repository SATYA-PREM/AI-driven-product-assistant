import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { authApi, workspaceApi } from '../../api/client';
import { getActiveWorkspaceId } from '../../utils/workspaceAccess';

const ROLES = [
  'Designer',
  'Developer',
  'Tester',
  'DevOps',
  'Stakeholder',
  'Research & Development',
];

export default function Login() {
  const navigate = useNavigate();
  const location = useLocation();

  const [form, setForm] = useState({
    email: '',
    password: '',
  });

  const [selectedRole, setSelectedRole] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;

    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError('');

    if (!form.email.trim()) {
      setError('Please enter your email.');
      return;
    }

    if (!form.password) {
      setError('Please enter your password.');
      return;
    }

    if (!selectedRole) {
      setError('Please select your role.');
      return;
    }

    try {
      setLoading(true);

      // 1. Actual backend authentication
      const loginResponse = await authApi.login({
        email: form.email.trim(),
        password: form.password,
      });

      /*
       * authApi.login() already stores access_token
       * using setStoredToken() inside client.js.
       */

      // 2. Store complete current user/session response
      const user = loginResponse?.user || loginResponse?.data?.user || null;

      if (user) {
        localStorage.setItem(
          'currentUser',
          JSON.stringify({
            ...user,
            token:
              loginResponse?.access_token ||
              loginResponse?.token ||
              user.token ||
              user.access_token,
          })
        );
      } else {
        // Still keep a valid session object so ProtectedRoutes
        // can recognize the authenticated user.
        localStorage.setItem(
          'currentUser',
          JSON.stringify({
            email: form.email.trim(),
            token:
              loginResponse?.access_token ||
              loginResponse?.token ||
              '',
          })
        );
      }

      // 3. Save selected frontend role
      localStorage.setItem('user_role', selectedRole);

      // 4. Try existing active workspace first
      let workspaceId = getActiveWorkspaceId();

      // 5. If there is no active workspace, get user's existing workspaces
      if (!workspaceId) {
        const workspaces = await workspaceApi.listWorkspaces();

        if (Array.isArray(workspaces) && workspaces.length > 0) {
          workspaceId =
            workspaces[0]?.id ||
            workspaces[0]?._id ||
            workspaces[0]?.workspace_id;
        }
      }

      /*
       * 6. If the user originally tried to open a protected route,
       * send them there after successful login.
       *
       * Otherwise open the existing workspace overview.
       */
      const requestedPath = location.state?.from?.pathname;

      if (
        requestedPath &&
        requestedPath !== '/login' &&
        workspaceId &&
        requestedPath.startsWith('/workspace/')
      ) {
        navigate(
          `${requestedPath}${location.state?.from?.search || ''}`,
          { replace: true }
        );
        return;
      }

      // 7. Existing workspace -> existing overview
      if (workspaceId) {
        localStorage.setItem('active_workspace_id', String(workspaceId));

        window.dispatchEvent(
          new CustomEvent('active_workspace_changed')
        );

        navigate(`/workspace/${workspaceId}/overview`, {
          replace: true,
        });

        return;
      }

      // 8. Authenticated but no workspace exists
      navigate('/workspaces', {
        replace: true,
      });
    } catch (err) {
      console.error('Login failed:', err);

      setError(
        err?.message ||
          'Login failed. Please check your email and password.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#070910] text-white flex items-center justify-center px-4 relative overflow-hidden">

      {/* Background glow */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-[-180px] left-1/2 -translate-x-1/2 w-[600px] h-[400px] bg-[#5b3df5]/15 blur-[140px] rounded-full" />

        <div className="absolute bottom-[-180px] right-[-100px] w-[450px] h-[350px] bg-purple-600/10 blur-[120px] rounded-full" />
      </div>

      {/* Grid */}
      <div className="absolute inset-0 bg-grid-pattern-dark opacity-30 pointer-events-none" />

      {/* Login Card */}
      <div className="relative z-10 w-full max-w-md">

        {/* Logo / Brand */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-gradient-to-br from-[#6d4aff] to-[#4324d8] shadow-lg shadow-purple-900/30 mb-4">
            <span className="text-xl font-black">P</span>
          </div>

          <h1 className="text-2xl font-bold tracking-tight">
            Product Intelligence
          </h1>

          <p className="text-sm text-slate-400 mt-2">
            Sign in to your workspace
          </p>
        </div>

        {/* Card */}
        <div className="bg-[#0d1019]/95 border border-white/10 rounded-2xl p-6 sm:p-7 shadow-2xl shadow-black/40 backdrop-blur-xl">

          <form onSubmit={handleSubmit}>

            {/* Email */}
            <div className="mb-5">
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Email
              </label>

              <input
                type="email"
                name="email"
                value={form.email}
                onChange={handleChange}
                placeholder="you@example.com"
                autoComplete="email"
                disabled={loading}
                className="w-full h-11 px-4 rounded-lg bg-[#080a11] border border-white/10 text-white placeholder:text-slate-600 outline-none transition focus:border-[#6d4aff] focus:ring-1 focus:ring-[#6d4aff]/40 disabled:opacity-50"
              />
            </div>

            {/* Password */}
            <div className="mb-5">
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Password
              </label>

              <input
                type="password"
                name="password"
                value={form.password}
                onChange={handleChange}
                placeholder="••••••••"
                autoComplete="current-password"
                disabled={loading}
                className="w-full h-11 px-4 rounded-lg bg-[#080a11] border border-white/10 text-white placeholder:text-slate-600 outline-none transition focus:border-[#6d4aff] focus:ring-1 focus:ring-[#6d4aff]/40 disabled:opacity-50"
              />
            </div>

            {/* Role */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-slate-300 mb-3">
                Select your role
              </label>

              <div className="grid grid-cols-2 gap-2">
                {ROLES.map((role) => {
                  const active = selectedRole === role;

                  return (
                    <button
                      key={role}
                      type="button"
                      disabled={loading}
                      onClick={() => {
                        setSelectedRole(role);
                        setError('');
                      }}
                      className={`
                        min-h-[42px]
                        px-3
                        rounded-lg
                        border
                        text-xs
                        font-medium
                        transition-all
                        text-left
                        ${
                          active
                            ? 'bg-[#5b3df5]/15 border-[#6d4aff] text-white shadow-[0_0_20px_rgba(91,61,245,0.12)]'
                            : 'bg-[#080a11] border-white/10 text-slate-400 hover:text-white hover:border-white/20'
                        }
                      `}
                    >
                      <span
                        className={`
                          inline-block w-1.5 h-1.5 rounded-full mr-2
                          ${
                            active
                              ? 'bg-[#8b75ff]'
                              : 'bg-slate-600'
                          }
                        `}
                      />

                      {role}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Error */}
            {error && (
              <div className="mb-5 rounded-lg border border-red-500/20 bg-red-500/10 px-3 py-2.5 text-sm text-red-300">
                {error}
              </div>
            )}

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="w-full h-11 rounded-lg bg-gradient-to-r from-[#6d4aff] to-[#5435e8] hover:from-[#795cff] hover:to-[#6245f0] text-white font-semibold text-sm transition-all shadow-lg shadow-purple-900/20 disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Signing in...
                </span>
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          <div className="mt-6 pt-5 border-t border-white/5 text-center">
            <p className="text-xs text-slate-600">
              Secure access to your Product Intelligence workspace
            </p>
          </div>
        </div>

        <p className="text-center text-xs text-slate-600 mt-6">
          Product Intelligence Platform
        </p>
      </div>
    </div>
  );
}