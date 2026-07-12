import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Leaf } from 'lucide-react';
import { login, getMe, register } from './authService';
import { useAuthStore } from '../../core/authStore';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { setToken, setUser } = useAuthStore();
  const [isLogin, setIsLogin] = useState(true);
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [isAdmin, setIsAdmin] = useState(false);
  
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      if (isLogin) {
        const { access_token } = await login(email, password);
        setToken(access_token);
        const me = await getMe();
        setUser(me);
        navigate('/dashboard');
      } else {
        await register({
          email,
          password,
          first_name: firstName,
          last_name: lastName,
          is_superuser: isAdmin
        });
        // Auto-login after successful registration
        const { access_token } = await login(email, password);
        setToken(access_token);
        const me = await getMe();
        setUser(me);
        navigate('/dashboard');
      }
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex bg-canvas">
      {/* Left Panel */}
      <div className="hidden lg:flex flex-col w-1/2 bg-[#1c2b27] p-12 justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-brand-green flex items-center justify-center">
            <Leaf className="w-4 h-4 text-white" />
          </div>
          <span className="text-white font-bold text-xl tracking-tight">Eco-fy</span>
        </div>
        <div>
          <blockquote className="text-white/70 text-lg leading-relaxed mb-6">
            "The world's most intelligent ESG Operating System. Move from compliance to competitive advantage."
          </blockquote>
          <div className="grid grid-cols-3 gap-4">
            {[
              { label: 'Organizations', value: '2,400+' },
              { label: 'CO₂ Tracked', value: '48Mt' },
              { label: 'Employee Actions', value: '12M+' },
            ].map((stat) => (
              <div key={stat.label} className="bg-white/5 rounded-card p-4">
                <p className="text-white font-bold text-2xl">{stat.value}</p>
                <p className="text-white/50 text-xs mt-1">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Right Panel */}
      <div className="flex-1 flex items-center justify-center p-8 overflow-y-auto">
        <div className="w-full max-w-sm py-8">
          <div className="mb-8">
            <div className="flex items-center gap-2 mb-6 lg:hidden">
              <Leaf className="w-5 h-5 text-brand-green" />
              <span className="font-bold text-lg text-on-surface">Eco-fy</span>
            </div>
            <h1 className="text-3xl font-bold tracking-tight mb-2">
              {isLogin ? 'Welcome back' : 'Create an account'}
            </h1>
            <p className="text-outline-variant">
              {isLogin ? 'Sign in to your ESG Operating System' : 'Get started with Eco-fy'}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <div className="flex gap-4">
                <div className="flex-1">
                  <label className="text-sm font-medium text-on-surface-variant mb-1.5 block">First Name</label>
                  <Input
                    type="text"
                    placeholder="John"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    required
                  />
                </div>
                <div className="flex-1">
                  <label className="text-sm font-medium text-on-surface-variant mb-1.5 block">Last Name</label>
                  <Input
                    type="text"
                    placeholder="Doe"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    required
                  />
                </div>
              </div>
            )}
            <div>
              <label className="text-sm font-medium text-on-surface-variant mb-1.5 block">Email</label>
              <Input
                id="email"
                type="email"
                placeholder="you@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div>
              <label className="text-sm font-medium text-on-surface-variant mb-1.5 block">Password</label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            {!isLogin && (
              <div className="flex items-center gap-2 pt-2">
                <input
                  type="checkbox"
                  id="isAdmin"
                  checked={isAdmin}
                  onChange={(e) => setIsAdmin(e.target.checked)}
                  className="w-4 h-4 text-brand-green rounded border-border-color focus:ring-brand-green"
                />
                <label htmlFor="isAdmin" className="text-sm text-on-surface-variant cursor-pointer">
                  Register as Admin (For testing purposes)
                </label>
              </div>
            )}
            
            {error && (
              <p className="text-error text-sm bg-error-container rounded-input px-3 py-2">{error}</p>
            )}
            
            <Button id="login-btn" type="submit" className="w-full mt-2" disabled={loading}>
              {loading ? 'Processing...' : isLogin ? 'Sign in' : 'Create account'}
            </Button>
          </form>
          
          <div className="mt-6 text-center text-sm">
            <span className="text-on-surface-variant">
              {isLogin ? "Don't have an account? " : "Already have an account? "}
            </span>
            <button
              type="button"
              onClick={() => {
                setIsLogin(!isLogin);
                setError('');
              }}
              className="text-brand-green font-semibold hover:underline"
            >
              {isLogin ? 'Sign up' : 'Sign in'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
