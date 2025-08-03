import React, { useState, useEffect, ReactNode } from 'react';
import styled, { DefaultTheme, ThemeProvider, css } from 'styled-components';
import { health } from './api';

// Extend the styled-components DefaultTheme to include our theme properties
declare module 'styled-components' {
  export interface DefaultTheme {
    colors: {
      primary: string;
      primaryHover: string;
      success: string;
      successLight: string;
      danger: string;
      dangerLight: string;
      text: string;
      textSecondary: string;
      background: string;
      cardBg: string;
      border: string;
    };
  }
}

// Helper type for styled components with theme
type ThemedStyledProps<P = {}> = P & {
  theme: DefaultTheme;
};

// Type definitions for styled-components props
interface StatusBadgeProps {
  status: boolean;
  theme: DefaultTheme;
}

// Theme configuration
const theme: DefaultTheme = {
  colors: {
    primary: '#4f46e5',
    primaryHover: '#4338ca',
    success: '#16a34a',
    successLight: '#dcfce7',
    danger: '#dc2626',
    dangerLight: '#fee2e2',
    text: '#1a1a1a',
    textSecondary: '#718096',
    background: '#f8fafc',
    cardBg: '#ffffff',
    border: '#e2e8f0',
  },
};

// Styled Components
const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: ${(props: ThemedStyledProps) => props.theme.colors.text};
`;

const Header = styled.header`
  text-align: center;
  margin-bottom: 3rem;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  font-weight: 700;
  color: ${(props: ThemedStyledProps) => props.theme.colors.primary};
  margin: 0 0 0.5rem;
`;

const Subtitle = styled.p`
  font-size: 1.25rem;
  color: ${(props: ThemedStyledProps) => props.theme.colors.textSecondary};
  margin: 0;
`;

const Card = styled.div`
  background: ${(props: ThemedStyledProps) => props.theme.colors.cardBg};
  border: 1px solid ${(props: ThemedStyledProps) => props.theme.colors.border};
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
`;

interface ButtonProps {
  disabled?: boolean;
  theme: DefaultTheme;
}

const Button = styled.button<ButtonProps>`
  background: ${(props: ThemedStyledProps<ButtonProps>) => props.theme.colors.primary};
  color: white;
  border: none;
  border-radius: 6px;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
  opacity: ${(props: ButtonProps) => (props.disabled ? 0.7 : 1)};
  pointer-events: ${(props: ButtonProps) => (props.disabled ? 'none' : 'auto')};

  &:hover {
    background: ${(props: ThemedStyledProps<ButtonProps>) => props.theme.colors.primaryHover};
  }
`;

const StatusBadge = styled.span<StatusBadgeProps>`
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
  background: ${(props: StatusBadgeProps) =>
    props.status ? props.theme.colors.successLight : props.theme.colors.dangerLight};
  color: ${(props: StatusBadgeProps) =>
    props.status ? props.theme.colors.success : props.theme.colors.danger};
  margin-left: 0.75rem;
  
  &::before {
    content: '';
    display: inline-block;
    width: 0.5rem;
    height: 0.5rem;
    border-radius: 50%;
    background: ${(props: StatusBadgeProps) =>
      props.status ? props.theme.colors.success : props.theme.colors.danger};
    margin-right: 0.375rem;
  }
`;

const Spinner = styled.span`
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
  margin-right: 0.5rem;
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
`;

const DataContainer = styled.pre`
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1.5rem;
  margin-top: 1.5rem;
  overflow-x: auto;
  font-size: 0.875rem;
  line-height: 1.5;
  color: #334155;
`;

// Main App Component
function AppContent() {
  const [data, setData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const checkHealth = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await health();
      setData(result);
    } catch (err) {
      setError('Falha ao conectar com a API. Verifique se o servidor está rodando.');
      console.error('API Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Check API health on component mount
  useEffect(() => {
    checkHealth();
  }, []);

  return (
    <Container>
      <Header>
        <Title>WatchTower AI</Title>
        <Subtitle>Monitoramento Inteligente de EPIs</Subtitle>
      </Header>

      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 style={{ margin: 0, fontSize: '1.5rem', color: '#2d3748' }}>
            Status da API
            {data && (
              <StatusBadge status={data?.status === 'ok'}>
                {data?.status === 'ok' ? 'Online' : 'Offline'}
              </StatusBadge>
            )}
          </h2>
          <Button onClick={checkHealth} disabled={isLoading}>
            {isLoading ? (
              <>
                <Spinner />
                Verificando...
              </>
            ) : (
              'Atualizar Status'
            )}
          </Button>
        </div>

        <div style={{ marginTop: '1.5rem' }}>
          <h3 style={{ margin: '0 0 0.5rem', color: '#4a5568' }}>Detalhes da API:</h3>
          {error ? (
            <div style={{ color: '#dc2626', backgroundColor: '#fef2f2', padding: '1rem', borderRadius: '8px' }}>
              {error}
            </div>
          ) : data ? (
            <DataContainer>
              <code>{JSON.stringify(data, null, 2)}</code>
            </DataContainer>
          ) : (
            <div style={{ color: '#64748b', fontStyle: 'italic' }}>
              Conectando ao servidor...
            </div>
          )}
        </div>
      </Card>

      <style jsx global>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * {
          box-sizing: border-box;
          margin: 0;
          padding: 0;
        }
        
        body {
          background-color: #f8fafc;
          color: #1a1a1a;
          font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          line-height: 1.5;
          -webkit-font-smoothing: antialiased;
          -moz-osx-font-smoothing: grayscale;
        }
      `}</style>
    </Container>
  );
}

// Wrap the app with ThemeProvider
export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <AppContent />
    </ThemeProvider>
  );
}
