import './css/App.css';
import 'bootstrap/dist/css/bootstrap.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Container } from 'react-bootstrap';
import Header from './components/Header';
import Footer from './components/Footer';
import HomeScreen from './screens/HomeScreen';
import UniversityScreen from './screens/UniversityScreen';
import CurrencyScreen from './screens/CurrencyScreen';
import DocumentsScreen from './screens/DocumentsScreen';
import ForumScreen from './screens/ForumScreen';
import MapScreen from './screens/MapScreen';
import NewsScreen from './screens/NewsScreen';
import QaScreen from './screens/QaScreen';
import HomeContentScreen from './screens/HomeContentScreen';
import CourseScreen from './screens/CourseScreen';
import { UnivercityProvider } from './context/uni/UnivercityContext';
import { AuthProvider } from './context/auth/AuthContext';
import TopicContainer from './components/forum/TopicContainer';
import ThreadContainer from './components/forum/ThreadContainer';
import ModalContainer from './components/auth/ModalContainer';
import { NewsContextProvider } from './NewsContext';
import News from './components/News';
import HomeTextComponent from './components/HomeTextComponent';

import NotFound from './components/NotFound';
import ProtectedRoute from './components/ProtectedRoute';
import UserProfileContainer from './components/auth/UserProfileContainer';

const App = () => {
  return (
    <AuthProvider>
      <UnivercityProvider>
        <Router>
          <>
            <HomeScreen />
            <Header title="Wroclaw Portal" />

            <main>
              <Container>
                <Routes>
                  <Route exact path="/currency" element={<CurrencyScreen />} />
                  <Route exact path="/uni" element={<UniversityScreen />} />
                  <Route exact path="/news" element={<NewsScreen />} />
                  <Route exact path="/map" element={<MapScreen />} />
                  <Route element={<ProtectedRoute />}>
                    <Route exact path="/forum" element={<ForumScreen />} />
                    <Route
                      exact
                      path="/users/:id"
                      element={<UserProfileContainer />}
                    />
                  </Route>
                  <Route exact path="/docs" element={<DocumentsScreen />} />
                  <Route exact path="/qa" element={<QaScreen />} />

                  <Route
                    exact
                    path="/courses/uni/:id"
                    element={<CourseScreen />}
                  />

                  <Route
                    exact
                    path="/forum/topics/:topic_id"
                    element={<TopicContainer />}
                  />
                  <Route
                    exact
                    path="/forum/:topic_id/threads/:id"
                    element={<ThreadContainer />}
                  />
                  <Route path="*" element={<NotFound />} />
                </Routes>
              </Container>
            </main>
            <ModalContainer />
            <Footer />
          </>
        </Router>
      </UnivercityProvider>
    </AuthProvider>
  );
};

export default App;
