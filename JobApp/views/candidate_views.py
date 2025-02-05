from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from JobApp.serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from JobApp.permissions import IsEmployer


@api_view(['GET'])
@permission_classes([IsEmployer])
def getCandidates(request):
    candidates = Candidate.objects.all()
    serializer = CandidateSerializer(candidates, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsEmployer])
def getCandidate(request, pk):
    try:
        candidate = Candidate.objects.get(id=pk)
        serializer = CandidateSerializer(candidate, many=False)
        return Response(serializer.data)
    except Candidate.DoesNotExist:
        return Response({'message': 'Candidate not found'}, status=404)


@api_view(['GET'])
@permission_classes([IsEmployer])
def getCandidateSkills(request, pk):
    if not Candidate.objects.filter(id=pk).exists():
        return Response({'message': 'Candidate not found.'}, status=404)
    candidate_skills = CandidateSkill.objects.filter(candidate_id=pk)
    if candidate_skills.exists():
        serializer = CandidateSkillSerializer(candidate_skills, many=True)
        return Response(serializer.data)
    else:
        return Response({'message': 'Candidate skills not found'}, status=404)


@api_view(['GET'])
@permission_classes([IsEmployer])
def getCandidateExperience(request, pk):
    if not Candidate.objects.filter(id=pk).exists():
        return Response({'message': 'Candidate not found'}, status=404)
    candidate_experience = CandidateExperience.objects.filter(candidate_id=pk)
    if candidate_experience.exists():
        serializer = CandidateExperienceSerializer(candidate_experience, many=True)
        return Response(serializer.data)
    else:
        return Response({'message': 'Candidate experience not found'}, status=404)


@api_view(['GET'])
@permission_classes([IsEmployer])
def getCandidateEducation(request, pk):
    if not Candidate.objects.filter(id=pk).exists():
        return Response({'message': 'Candidate not found'}, status=404)
    candidate_education = CandidateEducation.objects.filter(candidate_id=pk)
    if candidate_education.exists():
        serializer = CandidateEducationSerializer(candidate_education, many=True)
        return Response(serializer.data)
    else:
        return Response({'message': 'Candidate education not found'}, status=404)
