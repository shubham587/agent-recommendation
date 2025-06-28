import React, { useState } from 'react';
import {
  Box,
  Container,
  VStack,
  HStack,
  Heading,
  Text,
  Textarea,
  Button,
  Card,
  CardBody,
  CardHeader,
  Badge,
  Progress,
  Flex,
  SimpleGrid,
  Divider,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  Spinner,
  useToast,
  Icon,
  Wrap,
  WrapItem,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  List,
  ListItem,
  ListIcon,
} from '@chakra-ui/react';
import { FiCode, FiStar, FiTrendingUp, FiUsers, FiDollarSign, FiZap, FiCheck } from 'react-icons/fi';
import axios from 'axios';

const API_BASE_URL = process.env.NODE_ENV === 'production' ? '' : 'http://localhost:5001';

function App() {
  const [taskDescription, setTaskDescription] = useState('');
  const [recommendations, setRecommendations] = useState(null);
  const [taskAnalysis, setTaskAnalysis] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const toast = useToast();

  const handleRecommendation = async () => {
    if (!taskDescription.trim()) {
      toast({
        title: 'Task description required',
        description: 'Please enter a description of your coding task.',
        status: 'warning',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/recommend`, {
        task_description: taskDescription,
        top_n: 3
      });

      if (response.data.success) {
        setRecommendations(response.data.recommendations);
        setTaskAnalysis(response.data.task_analysis);
        toast({
          title: 'Recommendations generated!',
          description: 'Found the best AI coding agents for your task.',
          status: 'success',
          duration: 3000,
          isClosable: true,
        });
      } else {
        throw new Error(response.data.error || 'Failed to get recommendations');
      }
    } catch (err) {
      const errorMessage = err.response?.data?.error || err.message || 'Failed to get recommendations';
      setError(errorMessage);
      toast({
        title: 'Error',
        description: errorMessage,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const getPriceTierIcon = (tier) => {
    switch (tier) {
      case 'free': return { icon: FiCheck, color: 'green' };
      case 'freemium': return { icon: FiDollarSign, color: 'blue' };
      case 'paid': return { icon: FiDollarSign, color: 'orange' };
      default: return { icon: FiDollarSign, color: 'gray' };
    }
  };

  const getComplexityColor = (complexity) => {
    switch (complexity) {
      case 'beginner': return 'green';
      case 'intermediate': return 'yellow';
      case 'advanced': return 'red';
      default: return 'gray';
    }
  };

  const formatTaskType = (taskType) => {
    return taskType.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  return (
    <Box minH="100vh" bg="gray.50">
      {/* Header */}
      <Box bg="white" shadow="sm" borderBottom="1px" borderColor="gray.200">
        <Container maxW="container.xl" py={4}>
          <HStack spacing={3}>
            <Icon as={FiCode} boxSize={8} color="brand.500" />
            <VStack align="start" spacing={0}>
              <Heading size="lg" color="gray.800">
                AI Coding Agent Recommender
              </Heading>
              <Text color="gray.600" fontSize="sm">
                Find the perfect AI coding assistant for your projects
              </Text>
            </VStack>
          </HStack>
        </Container>
      </Box>

      <Container maxW="container.xl" py={8}>
        <VStack spacing={8} align="stretch">
          {/* Task Input Section */}
          <Card>
            <CardHeader>
              <Heading size="md" color="gray.700">
                Describe Your Coding Task
              </Heading>
              <Text color="gray.600" mt={2}>
                Tell us about your project, programming language, complexity, and any specific requirements.
              </Text>
            </CardHeader>
            <CardBody>
              <VStack spacing={4}>
                <Textarea
                  placeholder="e.g., I want to build a React web application with user authentication, database integration, and deployment to AWS. I'm a beginner looking for an AI assistant that can help me learn while building."
                  value={taskDescription}
                  onChange={(e) => setTaskDescription(e.target.value)}
                  rows={4}
                  bg="white"
                  borderColor="gray.300"
                  _focus={{ borderColor: 'brand.400', boxShadow: '0 0 0 1px #0087FF' }}
                />
                <Button
                  colorScheme="brand"
                  size="lg"
                  onClick={handleRecommendation}
                  isLoading={isLoading}
                  loadingText="Analyzing..."
                  leftIcon={<FiTrendingUp />}
                  w="full"
                >
                  Get AI Agent Recommendations
                </Button>
              </VStack>
            </CardBody>
          </Card>

          {/* Error Alert */}
          {error && (
            <Alert status="error" borderRadius="md">
              <AlertIcon />
              <AlertTitle>Error!</AlertTitle>
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {/* Task Analysis */}
          {taskAnalysis && (
            <Card>
              <CardHeader>
                <Heading size="md" color="gray.700">Task Analysis</Heading>
              </CardHeader>
              <CardBody>
                <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={4}>
                  <Stat>
                    <StatLabel>Task Type</StatLabel>
                    <StatNumber fontSize="lg">{formatTaskType(taskAnalysis.task_type)}</StatNumber>
                  </Stat>
                  <Stat>
                    <StatLabel>Complexity</StatLabel>
                    <StatNumber fontSize="lg">
                      <Badge colorScheme={getComplexityColor(taskAnalysis.complexity)} variant="subtle" px={2} py={1}>
                        {taskAnalysis.complexity}
                      </Badge>
                    </StatNumber>
                  </Stat>
                  <Stat>
                    <StatLabel>Context</StatLabel>
                    <StatNumber fontSize="lg">{taskAnalysis.context}</StatNumber>
                  </Stat>
                  <Stat>
                    <StatLabel>Languages</StatLabel>
                    <StatHelpText>
                      <Wrap>
                        {taskAnalysis.languages.length > 0 ? (
                          taskAnalysis.languages.map((lang, index) => (
                            <WrapItem key={index}>
                              <Badge colorScheme="blue" variant="outline">{lang}</Badge>
                            </WrapItem>
                          ))
                        ) : (
                          <Text fontSize="sm" color="gray.500">General</Text>
                        )}
                      </Wrap>
                    </StatHelpText>
                  </Stat>
                </SimpleGrid>
              </CardBody>
            </Card>
          )}

          {/* Loading State */}
          {isLoading && (
            <Card>
              <CardBody>
                <VStack spacing={4} py={8}>
                  <Spinner size="xl" color="brand.500" />
                  <Text color="gray.600">Analyzing your task and finding the best AI coding agents...</Text>
                </VStack>
              </CardBody>
            </Card>
          )}

          {/* Recommendations */}
          {recommendations && recommendations.length > 0 && (
            <VStack spacing={6} align="stretch">
              <Heading size="lg" color="gray.700" textAlign="center">
                🏆 Top Recommendations for Your Task
              </Heading>

              {recommendations.map((rec, index) => {
                const priceInfo = getPriceTierIcon(rec.price_tier);
                return (
                  <Card key={rec.agent_id} borderWidth="2px" borderColor={index === 0 ? "brand.200" : "gray.200"}>
                    <CardBody>
                      <VStack spacing={4} align="stretch">
                        {/* Header */}
                        <Flex justify="space-between" align="center" wrap="wrap">
                          <HStack spacing={3}>
                            <Badge colorScheme="brand" variant="solid" fontSize="sm" px={2} py={1}>
                              #{rec.rank}
                            </Badge>
                            <Heading size="lg" color="gray.800">
                              {rec.agent_name}
                            </Heading>
                            <Icon as={priceInfo.icon} color={`${priceInfo.color}.500`} />
                            <Badge colorScheme={priceInfo.color} variant="outline">
                              {rec.price_tier}
                            </Badge>
                          </HStack>
                          <VStack spacing={1} align="end">
                            <Text fontSize="2xl" fontWeight="bold" color="brand.500">
                              {rec.confidence}%
                            </Text>
                            <Text fontSize="sm" color="gray.500">
                              Confidence
                            </Text>
                          </VStack>
                        </Flex>

                        {/* Description */}
                        <Text color="gray.600" fontSize="md">
                          {rec.description}
                        </Text>

                        {/* Explanation */}
                        <Box bg="brand.50" p={4} borderRadius="md" borderLeft="4px" borderLeftColor="brand.400">
                          <Text color="gray.700" fontWeight="medium" mb={2}>
                            Why this agent is perfect for your task:
                          </Text>
                          <Text color="gray.600">
                            {rec.explanation}
                          </Text>
                        </Box>

                        {/* Progress Bar */}
                        <Box>
                          <Flex justify="space-between" mb={2}>
                            <Text fontSize="sm" color="gray.600">Match Score</Text>
                            <Text fontSize="sm" color="gray.600">{(rec.score * 100).toFixed(1)}%</Text>
                          </Flex>
                          <Progress value={rec.score * 100} colorScheme="brand" size="lg" borderRadius="md" />
                        </Box>

                        <Divider />

                        {/* Details */}
                        <SimpleGrid columns={{ base: 1, lg: 2 }} spacing={6}>
                          {/* Key Strengths */}
                          <Box>
                            <Text fontWeight="semibold" color="gray.700" mb={3}>
                              <Icon as={FiStar} mr={2} />
                              Key Strengths
                            </Text>
                            <List spacing={2}>
                              {rec.strengths.slice(0, 4).map((strength, idx) => (
                                <ListItem key={idx} color="gray.600">
                                  <ListIcon as={FiCheck} color="green.500" />
                                  {strength}
                                </ListItem>
                              ))}
                            </List>
                          </Box>

                          {/* Capabilities */}
                          <Box>
                            <Text fontWeight="semibold" color="gray.700" mb={3}>
                              <Icon as={FiZap} mr={2} />
                              Capabilities
                            </Text>
                            <Wrap>
                              {rec.capabilities.slice(0, 6).map((capability, idx) => (
                                <WrapItem key={idx}>
                                  <Badge colorScheme="purple" variant="outline">
                                    {capability}
                                  </Badge>
                                </WrapItem>
                              ))}
                            </Wrap>
                          </Box>
                        </SimpleGrid>

                        {/* Supported Languages */}
                        <Box>
                          <Text fontWeight="semibold" color="gray.700" mb={3}>
                            <Icon as={FiCode} mr={2} />
                            Supported Languages
                          </Text>
                          <Wrap>
                            {rec.supported_languages.slice(0, 8).map((lang, idx) => (
                              <WrapItem key={idx}>
                                <Badge colorScheme="teal" variant="subtle">
                                  {lang}
                                </Badge>
                              </WrapItem>
                            ))}
                            {rec.supported_languages.length > 8 && (
                              <WrapItem>
                                <Badge colorScheme="gray" variant="subtle">
                                  +{rec.supported_languages.length - 8} more
                                </Badge>
                              </WrapItem>
                            )}
                          </Wrap>
                        </Box>

                        {/* Score Breakdown - Collapsible */}
                        <Accordion allowToggle>
                          <AccordionItem border="none">
                            <AccordionButton px={0} _hover={{ bg: 'transparent' }}>
                              <Box flex="1" textAlign="left">
                                <Text fontWeight="semibold" color="gray.700">
                                  View Detailed Score Breakdown
                                </Text>
                              </Box>
                              <AccordionIcon />
                            </AccordionButton>
                            <AccordionPanel px={0} pt={4}>
                              <SimpleGrid columns={{ base: 1, md: 2 }} spacing={4}>
                                {Object.entries(rec.score_breakdown).map(([criterion, score]) => (
                                  <Box key={criterion}>
                                    <Flex justify="space-between" mb={1}>
                                      <Text fontSize="sm" color="gray.600" textTransform="capitalize">
                                        {criterion.replace('_', ' ')}
                                      </Text>
                                      <Text fontSize="sm" color="gray.600">
                                        {(score * 100).toFixed(1)}%
                                      </Text>
                                    </Flex>
                                    <Progress value={score * 100} size="sm" colorScheme="brand" borderRadius="sm" />
                                  </Box>
                                ))}
                              </SimpleGrid>
                            </AccordionPanel>
                          </AccordionItem>
                        </Accordion>
                      </VStack>
                    </CardBody>
                  </Card>
                );
              })}
            </VStack>
          )}

          {/* Footer */}
          <Box textAlign="center" py={8}>
            <Text color="gray.500" fontSize="sm">
              Built with ❤️ using Flask, React, and Chakra UI
            </Text>
          </Box>
        </VStack>
      </Container>
    </Box>
  );
}

export default App; 